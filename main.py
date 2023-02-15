import streamlit as st 
import pandas as pd
import numpy as np
import time 
import datetime

pd.options.display.float_format = '{:,.0f}'.format

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


def disp_acq_tables(current):
    
    last = current.last_valid_index() + 1

    data_disposed = {}
    data_acquired = {}


    for ind in range(last):
        
        if current['Agent 1'].loc[ind] not in data_disposed.keys():
            
            data_disposed.update({current['Agent 1'].loc[ind]:current['Total ft 2'].loc[ind]})
            
        else:
            
            data_disposed.update({current['Agent 1'].loc[ind]:current['Total ft 2'].loc[ind]+data_disposed[current['Agent 1'].loc[ind]]})
            
        if current['Agent 2'].loc[ind] not in data_disposed.keys():
            
            data_disposed.update({current['Agent 2'].loc[ind]:current['Total ft 2'].loc[ind]})
            
        else:
            
            data_disposed.update({current['Agent 2'].loc[ind]:current['Total ft 2'].loc[ind]+data_disposed[current['Agent 2'].loc[ind]]})
            
        if current['Agent 3'].loc[ind] not in data_disposed.keys():
            
            data_disposed.update({current['Agent 3'].loc[ind]:current['Total ft 2'].loc[ind]})
            
        else:
            
            data_disposed.update({current['Agent 3'].loc[ind]:current['Total ft 2'].loc[ind]+data_disposed[current['Agent 3'].loc[ind]]})
            
        if current['Lessee Agent'].loc[ind] not in data_acquired.keys():
            
            data_acquired.update({current['Lessee Agent'].loc[ind]:current['Total ft 2'].loc[ind]})
            
        else:
            
            data_acquired.update({current['Lessee Agent'].loc[ind]:current['Total ft 2'].loc[ind]+data_acquired[current['Lessee Agent'].loc[ind]]})
        

    disp = pd.DataFrame.from_dict(data_disposed,orient="index").sort_values(0,ascending=False).reset_index().dropna()
    disp.rename(columns = {'index':'Agency', 0:'Size'}, inplace = True)
    acq = pd.DataFrame.from_dict(data_acquired,orient="index").sort_values(0,ascending=False).reset_index().dropna()
    acq.rename(columns = {'index':'Agency', 0:'Size'}, inplace = True)
    return(disp,acq)


def combined_tables(current):
    
    last = current.last_valid_index() + 1

    data = {}

    for ind in range(last):
        
        if current['Agent 1'].loc[ind] not in data.keys():
            
            data.update({current['Agent 1'].loc[ind]:current['Total ft 2'].loc[ind]})
            
        else:
            
            data.update({current['Agent 1'].loc[ind]:current['Total ft 2'].loc[ind]+data[current['Agent 1'].loc[ind]]})
            
        if current['Agent 2'].loc[ind] not in data.keys():
            
            data.update({current['Agent 2'].loc[ind]:current['Total ft 2'].loc[ind]})
            
        else:
            
            data.update({current['Agent 2'].loc[ind]:current['Total ft 2'].loc[ind]+data[current['Agent 2'].loc[ind]]})
            
        if current['Agent 3'].loc[ind] not in data.keys():
            
            data.update({current['Agent 3'].loc[ind]:current['Total ft 2'].loc[ind]})
            
        else:
            
            data.update({current['Agent 3'].loc[ind]:current['Total ft 2'].loc[ind]+data[current['Agent 3'].loc[ind]]})
            
        if current['Lessee Agent'].loc[ind] not in data.keys():
            
            data.update({current['Lessee Agent'].loc[ind]:current['Total ft 2'].loc[ind]})
            
        else:
            
            data.update({current['Lessee Agent'].loc[ind]:current['Total ft 2'].loc[ind]+data[current['Lessee Agent'].loc[ind]]})
        

    both = pd.DataFrame.from_dict(data,orient="index").sort_values(0,ascending=False).reset_index().dropna()
    both.rename(columns = {'index':'Agency', 0:'Size'}, inplace = True)
    return(both)
    

@st.cache
def convert_df(df):
    
    return df.to_csv()

@st.cache
def upload_as(data):
    
    df = pd.read_excel(data)
    
    return(df)

@st.cache
def upload_clh(data):

    CLH = pd.read_excel(data)
                        
    CLH['Date Taken'] = pd.to_datetime(CLH['Date Taken'],format="%Y-%m-%d")

    CLH['Year Taken'] = CLH['Date Taken'].dt.year
    
    CLH = CLH[(CLH["Lease Status"] == "Let") & (CLH["Year Taken"] != 2222)]
                                
    return(CLH)

def selections(CLH):
    
    yt= CLH['Year Taken'].tolist()
    
    options_i = np.unique(yt)
    options = [int(float(x)) for x in options_i]
    options.sort(reverse=True)
    
    markets = list(np.unique(CLH['Sub Market']))
    markets.insert(0, "All")
    
    return(options,markets)

def JLL_performance(JLL):
    
    pd.options.display.float_format = '{:.0f}'.format
    
    data = JLL[['Year Taken','Total ft 2']].groupby(['Year Taken']).sum()
    
    data = data.tail(10)   
    
    return(data)

                    
st.title("CLSE Data Tools")

tabs_font_css = """
<style>
button[data-baseweb="tab"] {
    font-size: 20px;
}
</style>
"""


platform_options = st.selectbox(
    label = "Select Platform",
    options = ['Agents Society','Central London Hub'],
    )


if platform_options == "Agents Society":
    
    try:
        uploaded_file_1 = st.file_uploader(label="Upload Initial File", key="upload1")

        if uploaded_file_1 is not None:
            
            df = upload_as(uploaded_file_1)

            with st.expander("See Uploaded Data"):
            
                st.write(df)
                    
    except:
        
        st.error("Upload error - Check the file type is xlsx and the first row are column headers.")

    try:
        uploaded_file_2 = st.file_uploader(label="Upload Comparison File",key="upload2")
       
        if uploaded_file_2 is not None:
        
            df1 = upload_as(uploaded_file_2)

            with st.expander("See Uploaded Data"):
            
                st.write(df1)
        
        if uploaded_file_1 is None and uploaded_file_2 is None:        
            st.warning("Ensure both uploaded .xlsx files have identical column headers.")
            
    except:
        uploaded_file_2 = None
        st.error("Upload error - Check the file type is xlsx and the first row are column headers.")
        
  
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
                
                st.warning("Please check the .xlsx files you have uploaded include the column headers in the first row.")
                    
                
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
            
elif platform_options == "Central London Hub":
    
    try:
        uploaded_file_1 = st.file_uploader(label="Upload File", key="upload1")

        if uploaded_file_1 is not None:
        
            CLH = upload_clh(uploaded_file_1)
                                    
            with st.expander("See Uploaded Data"):
            
                st.write(CLH)
            
    except:
        uploaded_file_1 = None
        st.error("Upload error - Check the file type is .xlsx and the first row are column headers.")     
  
    if uploaded_file_1 is not None:

        st.write(tabs_font_css, unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["   Combined League Table  ", "   Disposal League Table   ", "   Acquistion League Table   "])
        
        with tab1:
            
            st.write("Use this tab to generate a combined (disposal & acquisition) league table based on the uploaded CLH file.")
            
            options = selections(CLH)
            
            cy = st.selectbox(
            'Select Year',
            (options[0]),key=203)
            
            m = st.selectbox(
            'Select Submarket',
            (options[1]),key=210)
            
            if m == "All":
                
                current = (CLH[CLH['Year Taken']==cy])
                
            else:
                
                current = (CLH[(CLH['Year Taken']==cy) & (CLH['Sub Market']==m)])
            
            
            if len(current) > 0:
                    
                current = current.reset_index(drop=True)
            
                final = combined_tables(current)
                                
                final.index = np.arange(1, len(final) + 1)
   
                st.table(data=final.style.format(thousands=",", precision=0))
                            
                res = convert_df(final)
                    
                if res:
                    
                    st.download_button(
                    label="Download League Table as CSV",
                    data=res,
                    key = 100,
                    file_name='Combined League Table.csv',
                    mime='text/csv',)
            
            else:
                
                st.write("No results.")
                    
                        
        with tab2:
        
            st.write("Use this tab to generate a disposal league table based on the uploaded CLH file.")
            
            cy = st.selectbox(
            'Select Year',
            (options[0]),key=211)
            
            m = st.selectbox(
            'Select Submarket',
            (options[1]),key=212)
            
            if m == "All":
                
                current = (CLH[CLH['Year Taken']==cy])
                
            else:
                
                current = (CLH[(CLH['Year Taken']==cy) & (CLH['Sub Market']==m)])

            if len(current) > 0:
                
                current = current.reset_index(drop=True)
                
                final = disp_acq_tables(current)
                
                final_disp = final[0].reset_index(drop=True)
                
                final_disp.index = np.arange(1, len(final_disp) + 1)
                
                st.table(data=final_disp.style.format(thousands=",", precision=0))
                
                res = convert_df(final_disp)
                    
                if res:
                    
                    st.download_button(
                    label="Download League Table as CSV",
                    data=res,
                    key = 101,
                    file_name='Disposal League Table.csv',
                    mime='text/csv',)
                    
            else:
                
                st.write("No results.")
            
                        
        with tab3:
        
            st.write("Use this tab to generate an acquisiton league table based on the uploaded CLH file.")
            
            cy = st.selectbox(
            'Select Year',
            (options[0]),key=221)
            
            m = st.selectbox(
            'Select Submarket',
            (options[1]),key=222)
            
            if m == "All":
                
                current = (CLH[CLH['Year Taken']==cy])
                
            else:
                
                current = (CLH[(CLH['Year Taken']==cy) & (CLH['Sub Market']==m)])

            if len(current) > 0:
                
                current = current.reset_index(drop=True)
                
                final = disp_acq_tables(current)
                
                final_acq = final[1]
                
                final_acq.index = np.arange(1, len(final_acq) + 1)
                
                st.table(data=final_acq.style.format(thousands=",", precision=0))
                
                res = convert_df(final_acq)
                    
                if res:
                    
                    st.download_button(
                    label="Download League Table as CSV",
                    data=res,
                    key = 1,
                    file_name='Acquisition League Table.csv',
                    mime='text/csv',)
                    
            else:
                
                st.write("No results.")


                

