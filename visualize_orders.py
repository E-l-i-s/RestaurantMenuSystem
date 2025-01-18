import pandas as pd
import plotly.express as px

# Load the dataset
file_path = "C:/Users/elisa/Desktop/projects/uni/gp/orders.csv"  # Update this path
order_data = pd.read_csv(file_path)

# Data cleaning: Ensure 'Price' and 'amount' are numeric
order_data['Price'] = pd.to_numeric(order_data['Price'], errors='coerce')
order_data['amount'] = pd.to_numeric(order_data['amount'], errors='coerce')

# Drop rows with missing or invalid values in 'Price' or 'amount'
order_data = order_data.dropna(subset=['Price', 'amount'])

# Calculate total revenue for each item
order_data['Revenue'] = order_data['Price'] * order_data['amount']

# Group by 'Item Name' for calculations
summary = order_data.groupby('Item Name').agg(
    Total_Orders=('amount', 'sum'),
    Total_Revenue=('Revenue', 'sum')
).reset_index()

# Sort the summary for better plotting
summary = summary.sort_values(by=['Total_Revenue', 'Total_Orders'], ascending=False)

# Create an animated scatter plot
fig = px.scatter(
    summary,
    x="Item Name",
    y="Total_Revenue",
    size="Total_Revenue",  # Bubble size shows revenue
    color="Total_Orders",  # Color scale now represents total orders
    title="Most Profitable and Ordered Menu Items",
    labels={
        "Item Name": "Menu Item",
        "Total_Revenue": "Revenue ($)",
        "Total_Orders": "Order Count"
    },
    hover_data=["Total_Orders", "Total_Revenue"],
    color_continuous_scale=px.colors.sequential.Viridis  # Choose a visually appealing color scale
)

# Enhance the layout
fig.update_layout(
    xaxis_title="Menu Items",
    yaxis_title="Revenue ($)",
    title_font_size=22,
    title_font_family="Arial",
    template="plotly_dark",
    showlegend=True,
    coloraxis_colorbar=dict(
        title="Order Count",  # Color bar title now reflects orders
        ticks="outside",
        lenmode="fraction",
        len=0.8  # Adjust length of color bar
    )
)

# Add interactivity and visual enhancements
fig.update_traces(
    marker=dict(
        sizemode='area',
        line=dict(width=2, color='white')
    ),
    textposition='top center'
)

# Show the chart
fig.show()
