import streamlit as st 
import pandas as pd

st.set_page_config(layout="wide")

st.markdown(""" <style> .font {
font-size:25px ; font-family: 'Cooper Black'; color: #FF9633;} 
</style> """, unsafe_allow_html=True)

def find_new_additions(df,df1):
    
    file_1_ids = df['Advert ID'].to_list()
    file_2_ids = df1['Advert ID'].to_list()
    
    new_records = (list(set(file_2_ids) - set(file_1_ids)))
    
    new_file = (df1.loc[df1['Advert ID'].isin(new_records)])
    
    new_file = new_file.set_index("Advert ID")
    
    return(new_file)
    
    
def no_longer_listed(df,df1):
    
    file_1_ids = df['Advert ID'].to_list()
    file_2_ids = df1['Advert ID'].to_list()
    
    missing_records = (list(set(file_1_ids) - set(file_2_ids)))
    
    new_file = (df.loc[df['Advert ID'].isin(missing_records)])
    
    new_file = new_file.set_index("Advert ID")
    
    return(new_file)
    
    
def compare_existing_rows(df,df1):
    
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
    
    
password = st.sidebar.text_input("Password",type='password')

if st.sidebar.checkbox("Login"):
    
    if password == 'beatone':
               
        st.header("Agents Society Comparison Tool")
        
        tabs_font_css = """
        <style>
        button[data-baseweb="tab"] {
            font-size: 20px;
        }
        </style>
        """
      
        st.write(tabs_font_css, unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["   Updated Records  ", "   New Records Created   ", "   Removed Records   "])

        with tab1:
            
            st.write("Use this tab to identify records which have been recently updated.")
            
            uploaded_file_1 = st.file_uploader(label="Upload Initial AS Extract (.csv)",key="upload1")
            
            if uploaded_file_1 is not None:
            
                df = pd.read_csv(uploaded_file_1,encoding="unicode_escape")
                
                with st.expander("See Uploaded Data"):
                
                    st.write(df)
                    
            uploaded_file_2 = st.file_uploader(label="Upload Latest AS Extract (.csv)",key="upload2")
            
            if uploaded_file_2 is not None:
            
                df1 = pd.read_csv(uploaded_file_2,encoding="unicode_escape")
                
                with st.expander("See Uploaded Data"):
                
                    st.write(df1)
                    
            if uploaded_file_1 is not None and uploaded_file_2 is not None:
                
                result = compare_existing_rows(df,df1)

                st.write(result)
                
        with tab2:
            
            st.write("Use this tab to identify records which have been recently added.")
            
            uploaded_file_2 = st.file_uploader(label="Upload Initial AS Extract (.csv)",key="upload3")
            
            if uploaded_file_2 is not None:
            
                df = pd.read_csv(uploaded_file_2,encoding="unicode_escape")
                
                with st.expander("See Uploaded Data"):
                
                    st.write(df)
                    
            uploaded_file_3 = st.file_uploader(label="Upload Latest AS Extract (.csv)",key="upload4")
            
            if uploaded_file_3 is not None:
            
                df1 = pd.read_csv(uploaded_file_3,encoding="unicode_escape")
                
                with st.expander("See Uploaded Data"):
                
                    st.write(df1)
                    
            if uploaded_file_2 is not None and uploaded_file_3 is not None:
                
                result = find_new_additions(df,df1)

                st.write(result)
                
        with tab3:
            
            st.write("Use this tab to identify records which have been recently removed.")
            
            uploaded_file_4 = st.file_uploader(label="Upload Initial AS Extract (.csv)",key="upload5")
            
            if uploaded_file_4 is not None:
            
                df = pd.read_csv(uploaded_file_4,encoding="unicode_escape")
                
                with st.expander("See Uploaded Data"):
                
                    st.write(df)
                    
            uploaded_file_5 = st.file_uploader(label="Upload Latest AS Extract (.csv)",key="upload6")
            
            if uploaded_file_5 is not None:
            
                df1 = pd.read_csv(uploaded_file_5,encoding="unicode_escape")
                
                with st.expander("See Uploaded Data"):
                
                    st.write(df1)
                    
            if uploaded_file_4 is not None and uploaded_file_5 is not None:
                
                result = no_longer_listed(df,df1)

                st.write(result)