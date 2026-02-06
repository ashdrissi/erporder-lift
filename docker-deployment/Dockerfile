FROM frappe/erpnext:v15.25.0

# Copy custom elevator_extensions app
COPY apps/elevator_extensions /home/frappe/frappe-bench/apps/elevator_extensions

# Install the custom app
RUN cd /home/frappe/frappe-bench && \
    bench get-app elevator_extensions file:///home/frappe/frappe-bench/apps/elevator_extensions && \
    bench build --app elevator_extensions

# Set user
USER frappe

WORKDIR /home/frappe/frappe-bench
