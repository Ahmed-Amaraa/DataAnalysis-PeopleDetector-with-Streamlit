import streamlit as st

st.write(
        """
        ## Help Information

        ### File Upload:
        - You can upload a CSV file to the app.
        
        ### Data Preview:
        - Once you upload the file, you can see the data with a specified number of rows.
        - Use the slider to choose how many rows to display.

        ### Selecting Columns:
        - Use the **Multiselect** to choose which columns to display in the table.

        ### Data Description:
        - You can get two types of data descriptions:
            - **Basic (Metadata)**: Shows metadata about the dataset like column types and non-null counts.
            - **Statistics**: Shows statistical data for numerical columns such as mean, std, min, and more.

        ### Plotting:
        - You can choose the type of plot:
            - **Scatter Plot**
            - **Histogram**
            - **Bar Plot**
            - **Box Plot**
        
        ### Plot Customization:
        - For each plot, you can set the columns for **X-axis** and **Y-axis**.
        - If you want to **color** the plot by a column, you can choose a column from the dropdown. If you don’t want to color the plot, set the value to `'None'`.

        #### Special Notes:
        - For **Bar Plot**, you can use both **X-axis** and **Y-axis**.
        - For **Univariate Analysis** in **Bar Plot**, you can set the **Y-axis** to `'None'` to only use **X-axis**.
        """
    )