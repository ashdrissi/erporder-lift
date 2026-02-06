// Real-time volume calculation for Quotation
frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        calculate_total_volume(frm);
    }
});

frappe.ui.form.on('Quotation Item', {
    qty: function(frm, cdt, cdn) {
        calculate_total_volume(frm);
    },
    item_code: function(frm, cdt, cdn) {
        // Slight delay to wait for item fetch
        setTimeout(() => calculate_total_volume(frm), 500);
    },
    items_remove: function(frm) {
        calculate_total_volume(frm);
    }
});

function calculate_total_volume(frm) {
    let total_volume = 0;
    let items_to_fetch = [];
    
    // Collect all item codes
    frm.doc.items.forEach(item => {
        if (item.item_code) {
            items_to_fetch.push(item);
        }
    });
    
    if (items_to_fetch.length === 0) {
        frm.set_value('total_volume', 0);
        frm.set_value('recommended_transport', 'N/A');
        return;
    }
    
    // Fetch volumes for all items
    let promises = items_to_fetch.map(item => {
        return frappe.db.get_value('Item', item.item_code, 'volume').then(r => {
            let volume = (r.message && r.message.volume) || 0;
            return volume * item.qty;
        });
    });
    
    Promise.all(promises).then(volumes => {
        total_volume = volumes.reduce((sum, v) => sum + v, 0);
        frm.set_value('total_volume', total_volume);
        
        // Get recommendation
        get_transport_recommendation(frm, total_volume);
    });
}

function get_transport_recommendation(frm, volume) {
    if (volume <= 0) {
        frm.set_value('recommended_transport', 'N/A');
        return;
    }
    
    // Try to get settings
    frappe.db.get_single_value('Logistics Settings', 'lcl_max_volume').then(lcl_max => {
        lcl_max = lcl_max || 15;
        
        return Promise.all([
            frappe.db.get_single_value('Logistics Settings', 'container_20ft_max_volume'),
            frappe.db.get_single_value('Logistics Settings', 'container_40ft_max_volume'),
            frappe.db.get_single_value('Logistics Settings', 'container_40ft_hq_max_volume'),
            frappe.db.get_single_value('Logistics Settings', 'lcl_label'),
            frappe.db.get_single_value('Logistics Settings', 'container_20ft_label'),
            frappe.db.get_single_value('Logistics Settings', 'container_40ft_label'),
            frappe.db.get_single_value('Logistics Settings', 'container_40ft_hq_label')
        ]).then(values => {
            let c20_max = values[0] || 28;
            let c40_max = values[1] || 58;
            let c40hq_max = values[2] || 68;
            let lcl_label = values[3] || 'LCL (Shared Container) / Small Truck';
            let c20_label = values[4] || '20ft Container';
            let c40_label = values[5] || '40ft Container';
            let c40hq_label = values[6] || '40ft High Cube Container';
            
            let recommendation;
            if (volume < lcl_max) {
                recommendation = lcl_label;
            } else if (volume <= c20_max) {
                recommendation = c20_label;
            } else if (volume <= c40_max) {
                recommendation = c40_label;
            } else if (volume <= c40hq_max) {
                recommendation = c40hq_label;
            } else {
                let containers = Math.ceil(volume / c20_max);
                recommendation = `Multiple Containers (approx ${containers} x 20ft)`;
            }
            
            frm.set_value('recommended_transport', recommendation);
        });
    });
}
