import streamlit as st 
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.markdown(""" <style> .font {
font-size:25px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)

tabs_font_css = """
<style>
button[data-baseweb="tab"] {
    font-size: 20px;
}
</style>
"""

title_font_css = """
<style>
button[data-baseweb="tab"] {
    font-size: 20px;
}
</style>
"""

def find_new_additions(platform_options,df,df1):
    
    if platform_options == "Agents Society":
        
        file_1_ids = df['Advert ID'].to_list()
        file_2_ids = df1['Advert ID'].to_list()
        
        new_records = (list(set(file_2_ids) - set(file_1_ids)))
        
        new_file = (df1.loc[df1['Advert ID'].isin(new_records)])
        
        new_file = new_file.set_index("Advert ID")
    
        return(new_file)
    
    
def no_longer_listed(platform_options,df,df1):
    
    if platform_options == "Agents Society":
    
        file_1_ids = df['Advert ID'].to_list()
        file_2_ids = df1['Advert ID'].to_list()
        
        missing_records = (list(set(file_1_ids) - set(file_2_ids)))
        
        new_file = (df.loc[df['Advert ID'].isin(missing_records)])
        
        new_file = new_file.set_index("Advert ID")
        
        return(new_file)
    
   
def compare_existing_rows(platform_options,df,df1):
    
    if platform_options == "Agents Society":
        
        if 'Details Last Confirmed' in df.columns:
    
            df = df.drop(['Details Last Confirmed'], axis=1)            
            df1 = df1.drop(['Details Last Confirmed'], axis=1)
    
        
        file_1_ids = df['Advert ID'].to_list()
        file_2_ids = df1['Advert ID'].to_list()
        
        existing_records = (list(set(file_1_ids).intersection(file_2_ids)))

        new_file1 = (df.loc[df['Advert ID'].isin(existing_records)])
        new_file2 = (df1.loc[df1['Advert ID'].isin(existing_records)])
        
        df = pd.concat([new_file1, new_file2])
        df = df.reset_index(drop=True)
        df_gpby = df.groupby(list(df.columns))
        
        idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
        
        changed = df.reindex(idx)
        
        changed = changed.set_index("Advert ID")
        
        return(changed)

def report_changes(df):
    
    df = df.fillna(0)
    df['Column/s Changed'] = 0
          
    changed = []

    df = df.reset_index()
    
    list_advert_ids = np.unique(df['Advert ID'].tolist())
    
    for each in list_advert_ids:
        
        data = df.loc[df['Advert ID'] == each]
        
        index = data.head(1).index[0]
        index_1 = index+1
        
        columns_changed = []
        
        for each in df.columns:

            if len(set(data[each].tolist())) > 1:
                
                columns_changed.append(each)
   
        data.loc[[index,index_1],'Column/s Changed'] = ",".join(columns_changed)
     
        changed.append(data)
        
    new_df = pd.concat(changed)
    new_df = new_df.set_index("Column/s Changed")
    return(new_df)


@st.cache
def convert_df(df):
    
    return df.to_csv()

def remove_false_values(df):

    error_values = [",","-","??","/","&","(",")",".","$","???","%","*","_","+","=","!","@","#",":",";","?","~","[","]","`","??"]

    for each in df.columns:
        
        for error in error_values:
        
            if df[each].dtype == object:
                
                df[each] = df[each].str.replace(error,"",regex=False)
                
            else:
                
                df[each] = df[each].replace(error,"")
                
    return(df)
                    
st.title("Agents Society Comparison Tool")

tabs_font_css = """
<style>
button[data-baseweb="tab"] {
    font-size: 20px;
}
</style>
"""


platform_options = st.multiselect(
    label = "Select Platform",
    options = ['Agents Society'],
    # default = ["Select Platform"],
    )

if platform_options:
    
       if len(platform_options) > 1:

        st.warning("Please select 1 platform.")

if len(platform_options) == 1:
    
    try:
        uploaded_file_1 = st.file_uploader(label="Upload Initial File", key="upload1")

        if uploaded_file_1 is not None:
            
            df = pd.read_csv(uploaded_file_1,encoding="unicode_escape")
            
            df = remove_false_values(df)

            with st.expander("See Uploaded Data"):
            
                st.write(df)
                    
    except:
        
        st.write("Upload error.")

    try:
        uploaded_file_2 = st.file_uploader(label="Upload Comparison File",key="upload2")
       
        if uploaded_file_2 is not None:
        
            df1 = pd.read_csv(uploaded_file_2,encoding="unicode_escape")
            
            df1 = remove_false_values(df1)

            with st.expander("See Uploaded Data"):
            
                st.write(df1)
        
        if uploaded_file_1 is None and uploaded_file_2 is None:        
            st.warning("Ensure both uploaded files have identical column headers.")
            st.warning("Remove all commas (,) before uploading files in .csv format to avoid upload errors.")
            
    except:
        
        st.write("Upload error.")
        
  
    if uploaded_file_1 is not None and uploaded_file_2 is not None:

        st.write(tabs_font_css, unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["   Updated Records  ", "   New Records Created   ", "   Removed Records   "])

        with tab1:
            
            st.write("Use this tab to identify records which have been recently updated.")
            
            try:                
                result = compare_existing_rows(platform_options[0],df,df1)
                
                result_1 = report_changes(result)

                st.write(result_1)
                
                res = convert_df(result_1)
                
                if res:
                    
                    st.download_button(
                    label="Download results as CSV",
                    data=res,
                    key = 1,
                    file_name='Missing records.csv',
                    mime='text/csv',)
                        
            except:
                
                st.warning("Please check the .csv files you have uploaded include the column headers in the first row with no special characters.")
                    
                
        with tab2:
            
            st.write("Use this tab to identify records which have been recently added.")
                
            result = find_new_additions(platform_options[0],df,df1)

            st.write(result)
            
            res = convert_df(result)
            
            if res:
                
                st.download_button(
                label="Download results as CSV",
                data=res,
                key = 2,
                file_name='Missing records.csv',
                mime='text/csv',)
                
        with tab3:
            
            st.write("Use this tab to identify records which have been recently removed.")
    
            result = no_longer_listed(platform_options[0],df,df1)

            st.write(result)
            
            res = convert_df(result)
            
            if res:
            
                st.download_button(
                label="Download results as CSV",
                data=res,
                key = 3,
                file_name='Missing records.csv',
                mime='text/csv',)
            