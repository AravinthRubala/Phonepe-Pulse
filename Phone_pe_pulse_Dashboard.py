import streamlit as st
from streamlit_lottie import st_lottie
import plotly.express as px
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from PIL import Image
from git.repo.base import Repo
import mysql.connector
import requests
import pandas as pd
from sqlalchemy import create_engine 
from plotly.subplots import make_subplots

def connect_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rubala",
        database="PhonePe"
    )
    return mydb


mydb = connect_database()
query = mydb.cursor()


st.set_page_config(page_title="Phonepe Data Visualization webpage",layout="wide")
st.title('📱 :violet[ PhonePe Pulse Data Visualization ] ⚡')
st.sidebar.header("🙏🏻  :orange[**Hello! Welcome to the phonepe pulse dashboard**] ")


with st.sidebar:
    select=option_menu(None, ["About","Home", "Transaction","Users Data","Map","Top 10 States Data",'Feedback'], 
        icons=["bar-chart",'house','bank','search','globe',"toggles",'chat-dots'], 
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "red", "font-size": "25px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"},})
    
    year = st.slider("**Year**", min_value=2018, max_value=2023)
    quarter = st.slider("Quarter", min_value=1, max_value=4)

st.subheader(f"**:violet[Total INDIA Transaction Details- Q{quarter}, {year}]**")
col1i, col2i,col3i  = st.columns(3)
with col1i:
    qry1 = f"select sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_Transaction_Amount" \
            f" from agg_trans where Year={year} and Quarter={quarter}"
    IndiaTotal = pd.read_sql_query(qry1, mydb)
    st.write(f"**:orange[_All PhonePe Transactions(UPI+Cards+Wallets) :_] "
                 f":black[{round(IndiaTotal.iloc[0, 0])}]**")
with col2i:
    st.write(f"**:orange[_Total Payment Value :_] :black[Rs. {round(IndiaTotal.iloc[0, 1])}]**")
    Average_Transaction_Value = (IndiaTotal.iloc[0, 1]/IndiaTotal.iloc[0, 0])
with col3i:
    st.write(f"**:orange[_Average Transaction Value :_] :black[Rs. {round(Average_Transaction_Value)}]**")
st.write('---')

# with col3i:
#     st.write("**:orange[_Categories :_]**")
#     qry2 = f"select Transaction_Type, sum(Transaction_Count) as Transaction_Count, " \
#            f"sum(Transaction_Amount) as Transaction_Amount from agg_trans " \
#            f"where Year={year} and Quarter={quarter} group by Transaction_Type"
#     IndiaCategory = pd.read_sql_query(qry2, mydb)
#     st.dataframe(IndiaCategory)


image1=Image.open(r"C:\Users\Admin\Desktop\GUVI\Task_Phone_pe_pulse\My project\ICN.png")
# video_file=open("C:/Users/Admin/Desktop/GUVI/Task_Phone_pe_pulse/My project/about.mp4",'rb')
# video=video_file.read()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

lottie_m=load_lottieurl(r"https://assets4.lottiefiles.com/datafiles/5FGDT1tGd6PRFWjrlnK36tsX4dv7kt1ihUMebNma/india.json")

if select == "About":
    st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    col1,col2 = st.columns(2)
    with col1:
        st.image(image1)
        st.subheader("Phonepe Now Everywhere..!")
        st.video("C:/Users/Admin/Desktop/GUVI/Task_Phone_pe_pulse/My project/about.mp4")

    with col2:
        st_lottie(
            lottie_m,
            speed=0.1,
            reverse=False,
            loop=True,
            quality="low",
            height=500,
            width=None,
            key=None
            ) 

if select=="Home":
    col1,col2, = st.columns(2)
    st.image(image1,width = 500)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
    with col2:
        st.video("C:/Users/Admin/Desktop/GUVI/Task_Phone_pe_pulse/My project/upi.mp4")


# DATASETS
Data_Aggregated_Transaction_df= pd.read_csv(r"agg_trans.csv")
Data_Aggregated_User_Summary_df= pd.read_csv(r"agg_user_state_reg.csv")
Data_Aggregated_User_df= pd.read_csv(r"agg_user_state_brand.csv")
Scatter_Geo_Dataset =  pd.read_csv(r"Data_Map_Districts_Longitude_Latitude.csv")
Coropleth_Dataset =  pd.read_csv(r"Data_Map_IndiaStates_TU.csv")
Data_Map_Transaction_df = pd.read_csv(r"Data_Map_Transaction_Table.csv")
Data_Map_User_Table= pd.read_csv(r"map_user.csv")
Data_top_transaction= pd.read_csv(r"top_trans_district.csv")
Indian_States= pd.read_csv(r"Longitude_Latitude_State_Table.csv")

if select=='Map':
    c1,c2=st.columns(2)
    with c1:
        Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022'))
    with c2:
        Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'))
    year=int(Year)
    quarter=int(Quarter)
    Transaction_scatter_districts=Data_Map_Transaction_df.loc[(Data_Map_Transaction_df['Year'] == year ) & (Data_Map_Transaction_df['Quarter']==quarter) ].copy()
    Transaction_Coropleth_States=Transaction_scatter_districts[Transaction_scatter_districts["State"] == "india"]
    Transaction_scatter_districts.drop(Transaction_scatter_districts.index[(Transaction_scatter_districts["State"] == "india")],axis=0,inplace=True)
    
    Transaction_scatter_districts = Transaction_scatter_districts.sort_values(by=['Place_Name'], ascending=False)
    Scatter_Geo_Dataset = Scatter_Geo_Dataset.sort_values(by=['District'], ascending=False) 
    Total_Amount=[]
    for i in Transaction_scatter_districts['Total_Amount']:
        Total_Amount.append(i)
    Scatter_Geo_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_scatter_districts['Total_Transactions_count']:
        Total_Transaction.append(i)
    Scatter_Geo_Dataset['Total_Transactions']=Total_Transaction
    Scatter_Geo_Dataset['Year_Quarter']=str(year)+'-Q'+str(quarter)
    # Dynamic Coropleth
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['state'], ascending=False)
    Transaction_Coropleth_States = Transaction_Coropleth_States.sort_values(by=['Place_Name'], ascending=False)
    Total_Amount=[]
    for i in Transaction_Coropleth_States['Total_Amount']:
        Total_Amount.append(i)
    Coropleth_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_Coropleth_States['Total_Transactions_count']:
        Total_Transaction.append(i)
    Coropleth_Dataset['Total_Transactions']=Total_Transaction
        

    Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
    Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
    Indian_States['Total_Amount']=Coropleth_Dataset['Total_Amount']
    Indian_States['Total_Transactions']=Coropleth_Dataset['Total_Transactions']
    Indian_States['Year_Quarter']=str(year)+'-Q'+str(quarter)

    fig=px.scatter_geo(Indian_States,
                    lon=Indian_States['Longitude'],
                    lat=Indian_States['Latitude'],                                
                    text = Indian_States['code'], #It will display district names on map
                    hover_name="state", 
                    hover_data=['Total_Amount',"Total_Transactions","Year_Quarter"],
                    )
    fig.update_traces(marker=dict(color="white" ,size=0.3))
    fig.update_geos(fitbounds="locations", visible=False,)
        # scatter plotting districts
    Scatter_Geo_Dataset['col']=Scatter_Geo_Dataset['Total_Transactions']
    fig1=px.scatter_geo(Scatter_Geo_Dataset,
                        lon=Scatter_Geo_Dataset['Longitude'],
                        lat=Scatter_Geo_Dataset['Latitude'],
                        color=Scatter_Geo_Dataset['col'],
                        size=Scatter_Geo_Dataset['Total_Transactions'],     
                        #text = Scatter_Geo_Dataset['District'], #It will display district names on map
                        hover_name="District", 
                        hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                        title='District',
                        size_max=22,)
    fig1.update_traces(marker=dict(color="rebeccapurple" ,line_width=1))    #rebeccapurple
    #coropleth mapping india
    fig_ch = px.choropleth(
                        Coropleth_Dataset,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',                
                        locations='state',
                        color="Total_Transactions", 
                        # width = 800,
                        # height=800,                                     
                        )
    fig_ch.update_geos(fitbounds="locations", visible=False,)
    #combining districts states and coropleth
    fig_ch.add_trace( fig.data[0])
    fig_ch.add_trace(fig1.data[0])

    # st.write("### **:blue[PhonePe India Map]**")
    st.subheader(f"**:violet[PhonePe India Map- Q{quarter}, {year}]**")
    colT1,colT2 = st.columns([6,4])
    with colT1:
        st.plotly_chart(fig_ch, use_container_width=True)
    with colT2:
        st.info(
        """
        Details of Map:
        - The darkness of the state color represents the total transactions
        - The Size of the Circles represents the total transactions dictrict wise
        - The bigger the Circle the higher the transactions
        - Hover data will show the details like Total transactions, Total amount
        """
        )
        st.info(
        """
        Important Observations:
        - User can observe Transactions of PhonePe in both statewide and Districtwide.
        - We can clearly see the states with highest transactions in the given year and quarter
        - We get basic idea about transactions district wide
        """
        )
# -----------------------------------FIGURE2 HIDDEN BARGRAPH------------------------------------------------------------------------
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['Total_Transactions'])
    fig = px.bar(Coropleth_Dataset, x='state', y='Total_Transactions',title=str(year)+" Quarter-"+str(quarter))
    with st.expander("See Bar graph for the same data"):
        st.plotly_chart(fig, use_container_width=True)
        st.info('**:blue[The above bar graph showing the increasing order of PhonePe Transactions according to the states of India, Here we can observe the top states with highest Transaction by looking at graph]**')
        

if select=='Transaction':
    st.write('# :green[ :currency_exchange: TRANSACTIONS ANALYSIS :currency_exchange:]')
    tab1, tab2, tab3, tab4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS", "YEAR ANALYSIS", "OVERALL ANALYSIS"])
    #==================================================T FIGURE1 STATE ANALYSIS=======================================================
    with tab1:
        Data_Aggregated_Transaction=Data_Aggregated_Transaction_df.copy()
        Data_Aggregated_Transaction.drop(Data_Aggregated_Transaction.index[(Data_Aggregated_Transaction["State"] == "india")],axis=0,inplace=True)
        State_PaymentMode=Data_Aggregated_Transaction.copy()
        # st.write('### :green[State & PaymentMode]')
        col1, col2= st.columns(2)
        with col1:
            mode = st.selectbox(
                'Please select the Mode',
                ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='a')
        with col2:
            state = st.selectbox(
            'Please select the State',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
            'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
            'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
            'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal'),key='b')
        State= state
        Year_List=[2018,2019,2020,2021,2022,2023]
        Mode=mode
        State_PaymentMode=State_PaymentMode.loc[(State_PaymentMode['State'] == State ) & (State_PaymentMode['Year'].isin(Year_List)) & 
                                (State_PaymentMode['Transaction_Type']==Mode )]
        State_PaymentMode = State_PaymentMode.sort_values(by=['Year'])
        State_PaymentMode["Quarter"] = "Q"+State_PaymentMode['Quarter'].astype(str)
        State_PaymentMode["Year_Quarter"] = State_PaymentMode['Year'].astype(str) +"-"+ State_PaymentMode["Quarter"].astype(str)
        fig = px.bar(State_PaymentMode, x='Year_Quarter', y='Transaction_Count',color="Transaction_Count",
                    color_continuous_scale="Viridis")
        
        colT1,colT2 = st.columns([7,3])
        with colT1:
            st.write('#### '+State.upper()) 
            st.plotly_chart(fig,use_container_width=True)
        with colT2:
            st.info(
            """
            Details of BarGraph:
            - This entire data belongs to state selected by you
            - X Axis is basically all years with all quarters 
            - Y Axis represents total transactions in selected mode        
            """
            )
            st.info(
            """
            Important Observations:
            - User can observe the pattern of payment modes in a State 
            - We get basic idea about which mode of payments are either increasing or decreasing in a state
            """
            )
        #=============================================T FIGURE2 DISTRICTS ANALYSIS=============================================
        with tab2:
            col1, col2, col3= st.columns(3)
            with col1:
                Year = st.selectbox(
                    'Please select the Year',
                    ('2018', '2019', '2020','2021','2022','2023'),key='y1')
            with col2:
                state = st.selectbox(
                'Please select the State',
                ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                'uttarakhand', 'west-bengal'),key='dk')
            with col3:
                Quarter = st.selectbox(
                    'Please select the Quarter',
                    ('1', '2', '3','4'),key='qwe')
            districts=Data_Map_Transaction_df.loc[(Data_Map_Transaction_df['State'] == state ) & (Data_Map_Transaction_df['Year']==int(Year))
                                                & (Data_Map_Transaction_df['Quarter']==int(Quarter))]
            l=len(districts)    
            fig = px.bar(districts, x='Place_Name', y='Total_Transactions_count',color="Total_Transactions_count",
                        color_continuous_scale="Viridis")   
            colT1,colT2 = st.columns([7,3])
            with colT1:
                st.write('#### '+state.upper()+' WITH '+str(l)+' DISTRICTS')
                st.plotly_chart(fig,use_container_width=True)
            with colT2:
                st.info(
                """
                Details of BarGraph:
                - This entire data belongs to state selected by you
                - X Axis represents the districts of selected state
                - Y Axis represents total transactions        
                """
                )
                st.info(
                """
                Important Observations:
                - User can observe how transactions are happening in districts of a selected state 
                - We can observe the leading distric in a state 
                """
                )
    #=============================================T FIGURE3 YEAR ANALYSIS===================================================
        with tab3:
            #st.write('### :green[PaymentMode and Year]')
            col1, col2= st.columns(2)
            with col1:
                M = st.selectbox(
                    'Please select the Mode',
                    ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='D')
            with col2:
                Y = st.selectbox(
                'Please select the Year',
                ('2018', '2019', '2020','2021','2022','2023'),key='F')
            Year_PaymentMode=Data_Aggregated_Transaction.copy()
            Year=int(Y)
            Mode=M
            Year_PaymentMode=Year_PaymentMode.loc[(Year_PaymentMode['Year']==Year) & 
                                    (Year_PaymentMode['Transaction_Type']==Mode )]
            States_List=Year_PaymentMode['State'].unique()
            State_groupby_YP=Year_PaymentMode.groupby('State')
            Year_PaymentMode_Table=State_groupby_YP.sum()
            Year_PaymentMode_Table['states']=States_List
            del Year_PaymentMode_Table['Quarter'] # ylgnbu', 'ylorbr', 'ylorrd teal
            del Year_PaymentMode_Table['Year']
            Year_PaymentMode_Table = Year_PaymentMode_Table.sort_values(by=['Transaction_Count'])
            fig2= px.bar(Year_PaymentMode_Table, x='states', y='Transaction_Count',color="Transaction_Count",
                        color_continuous_scale="Viridis",)   
            colT1,colT2 = st.columns([7,3])
            with colT1:
                st.write('#### '+str(Year)+' DATA ANALYSIS')
                st.plotly_chart(fig2,use_container_width=True) 
            with colT2:
                st.info(
                """
                Details of BarGraph:
                - This entire data belongs to selected Year
                - X Axis is all the states in increasing order of Total transactions
                - Y Axis represents total transactions in selected mode        
                """
                )
                st.info(
                """
                Important Observations:
                - We can observe the leading state with highest transactions in particular mode
                - We get basic idea about regional performance of Phonepe
                - Depending on the regional performance Phonepe can provide offers to particular place
                """
                )
    #=============================================T FIGURE4 OVERALL ANALYSIS=============================================
        with tab4:    
            years=Data_Aggregated_Transaction.groupby('Year')
            years_List=Data_Aggregated_Transaction['Year'].unique()
            years_Table=years.sum()
            del years_Table['Quarter']
            years_Table['year']=years_List
            total_trans=years_Table['Transaction_Count'].sum() # this data is used in sidebar    
            fig1 = px.pie(years_Table, values='Transaction_Count', names='year',color_discrete_sequence=px.colors.sequential.Viridis, title='TOTAL TRANSACTIONS (2018 TO 2023)')
            col1, col2= st.columns([0.65,0.35])
            with col1:
                st.write('### :green[Drastical Increase in Transactions :rocket:]')
                st.plotly_chart(fig1)
            with col2:  
                st.write('#### :green[Year Wise Transaction Analysis in INDIA]')      
                st.markdown(years_Table.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                st.info(
                """
                Important Observations:
                - Its very clearly understood that online transactions drasticall increased
                - Initially in 2018,2019 the transactions are less but with time the online payments are increased at a high scale via PhonePe.
                - We can clearly see that more than 38.7% of total Phonepe transactions in india happened are from the year 2023
                """
                )

if select=='Users Data':
    st.write('# :green[USERS DATA ANALYSIS 🧑🏻‍💻 ]')
    tab1, tab2, tab3, tab4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS","YEAR ANALYSIS","OVERALL ANALYSIS"])
    # =================================================U STATE ANALYSIS ========================================================
    with tab1:
        st.write('### :blue[State & Userbase]')
        state = st.selectbox(
            'Please select the State',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
            'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
            'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
            'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal'),key='W')
        app_opening=Data_Aggregated_User_Summary_df.groupby(['State','Year'])
        a_state=app_opening.sum()
        la=Data_Aggregated_User_Summary_df['State'] +"-"+ Data_Aggregated_User_Summary_df["Year"].astype(str)
        a_state["state_year"] = la.unique()
        sta=a_state["state_year"].str[:-5]
        a_state["state"] = sta
        sout=a_state.loc[(a_state['state'] == state) ]
        ta=sout['App_Opens'].sum()
        tr=sout['Registered_Users'].sum()
        sout['App_Opens']=sout['App_Opens'].mul(100/ta)
        sout['Registered_Users']=sout['Registered_Users'].mul(100/tr).copy()
        fig = go.Figure(data=[
            go.Bar(name='App_Opens %', y=sout['App_Opens'], x=sout['state_year'], marker={'color': 'pink'}),
            go.Bar(name='Registered_Users %', y=sout['Registered_Users'], x=sout['state_year'],marker={'color': 'orange'})
        ])
        # Change the bar mode
        fig.update_layout(barmode='group')
        colT1,colT2 = st.columns([7,3])
        with colT1:
            st.write("#### ",state.upper())
            st.plotly_chart(fig, use_container_width=True, height=200)
        with colT2:
            st.info(
            """
            Details of BarGraph:
            - user need to select a state 
            - The X Axis shows both Registered users and App openings 
            - The Y Axis shows the Percentage of Registered users and App openings
            """
            )
            st.info(
            """
            Important Observations:
            - User can observe how the App Openings are growing and how Registered users are growing in a state
            - We can clearly obseve these two parameters with time
            - one can observe how user base is growing
            """
            )
        # ==================================================U DISTRICT ANALYSIS ====================================================
        with tab2:
            col1, col2, col3= st.columns(3)
            with col1:
                Year = st.selectbox(
                    'Please select the Year',
                    ('2023','2022', '2021','2020','2019','2018'),key='y12')
            with col2:
                state = st.selectbox(
                'Please select the State',
                ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                'uttarakhand', 'west-bengal'),key='dk2')
            with col3:
                Quarter = st.selectbox(
                    'Please select the Quarter',
                    ('1', '2', '3','4'),key='qwe2')
            districts=Data_Map_User_Table.loc[(Data_Map_User_Table['State'] == state ) & (Data_Map_User_Table['Year']==int(Year))
                                                & (Data_Map_User_Table['Quarter']==int(Quarter))]
            l=len(districts)    
            fig = px.bar(districts, x='District', y='App_Opens',color="App_Opens",
                        color_continuous_scale="reds")   
            colT1,colT2 = st.columns([7,3])
            with colT1:
                if l:
                    st.write('#### '+state.upper()+' WITH '+str(l)+' DISTRICTS')
                    st.plotly_chart(fig,use_container_width=True)
                else:
                    st.write('#### NO DISTRICTS DATA AVAILABLE FOR '+state.upper())

            with colT2:
                if l:
                    st.info(
                """
                Details of BarGraph:
                - This entire data belongs to state selected by you
                - X Axis represents the districts of selected state
                - Y Axis represents App Openings       
                """
                    )
                    st.info(
                """
                Important Observations:
                - User can observe how App Openings are happening in districts of a selected state 
                - We can observe the leading distric in a state 
                """
                    )
        # ==================================================U YEAR ANALYSIS ========================================================
        with tab3:
            st.write('### :orange[Brand Share] ')
            col1, col2= st.columns(2)
            with col1:
                state = st.selectbox(
                'Please select the State',
                ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                'uttarakhand', 'west-bengal'),key='Z')
            with col2:
                Y = st.selectbox(
                'Please select the Year',
                ('2018', '2019', '2020','2021','2022','2023'),key='X')
            y=int(Y)
            s=state
            brand=Data_Aggregated_User_df[Data_Aggregated_User_df['Year']==y] 
            brand=Data_Aggregated_User_df.loc[(Data_Aggregated_User_df['Year'] == y) & (Data_Aggregated_User_df['State'] ==s)]
            myb= brand['Brand'].unique()
            x = sorted(myb).copy()
            b=brand.groupby('Brand').sum()
            b['brand']=x
            br=b['Registration_Count'].sum()
            labels = b['brand']
            values = b['Registration_Count'] # customdata=labels,
            fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4,textinfo='label+percent',texttemplate='%{label}<br>%{percent:1%f}',insidetextorientation='horizontal',textfont=dict(color='#000000'),marker_colors=px.colors.qualitative.Prism)])
            
            colT1,colT2 = st.columns([7,3])
            with colT1:
                st.write("#### ",state.upper()+' IN '+Y)
                st.plotly_chart(fig3, use_container_width=True)        
            with colT2:
                st.info(
                """
                Details of Donut Chart:        
                - Initially we select data by means of State and Year
                - Percentage of registered users is represented with dounut chat through Device Brand
                """
                )
                st.info(
                """
                Important Observations:
                - User can observe the top leading brands in a particular state
                - Brands with less users
                - Brands with high users
                - Can make app download advices to growing brands
                """
                )

            b = b.sort_values(by=['Registration_Count'])
            fig4= px.bar(b, x='brand', y='Registration_Count',color="Registration_Count",
                        title='In '+state+'in '+str(y),
                        color_continuous_scale="oranges",)
            with st.expander("See Bar graph for the same data"):
                st.plotly_chart(fig4,use_container_width=True)
        # ===================================================U OVERALL ANALYSIS ====================================================

        with tab4:
            years=Data_Aggregated_User_Summary_df.groupby('Year')
            years_List=Data_Aggregated_User_Summary_df['Year'].unique()
            years_Table=years.sum()
            del years_Table['Quarter']
            years_Table['year']=years_List
            total_trans=years_Table['Registered_Users'].sum() # this data is used in sidebar    
            fig1 = px.pie(years_Table, values='Registered_Users', names='year',color_discrete_sequence=px.colors.sequential.RdBu, title='TOTAL REGISTERED USERS (2018 TO 2023)')
            col1, col2= st.columns([0.7,0.3])
            with col1:
                # st.write('### :green[Drastical Increase in Transactions :rocket:]')
                # labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
                #     "Rest of World"]

                # Create subplots: use 'domain' type for Pie subplot
                fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
                fig.add_trace(go.Pie(labels=years_Table['year'], values=years_Table['Registered_Users'], name="REGISTERED USERS"),
                            1, 1)
                fig.add_trace(go.Pie(labels=years_Table['year'], values=years_Table['App_Opens'], name="APP OPENS"),
                            1, 2)

                # Use `hole` to create a donut-like pie chart
                fig.update_traces(hole=.6, hoverinfo="label+percent+name")

                fig.update_layout(
                    title_text="USERS DATA (2018 TO 2023)",
                    # Add annotations in the center of the donut pies.
                    annotations=[dict(text='USERS', x=0.18, y=0.5, font_size=20, showarrow=False),
                                dict(text='APP', x=0.82, y=0.5, font_size=20, showarrow=False)])
                # st.plotly_chart(fig1)
                st.plotly_chart(fig)
            with col2:  
                # st.write('#### :green[Year Wise Transaction Analysis in INDIA]')      
                st.markdown(years_Table.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                st.info(
                """
                Important Observation:
                -  We can see that the Registered Users and App openings are increasing year by year
                
                """
                )

if select == "Top 10 States Data":
    c1,c2=st.columns(2)
    with c1:
        Year = st.selectbox(
                'Please select the Year',
                ('2023','2022', '2021','2020','2019','2018'),key='y1h2k')
    with c2:
        Quarter = st.selectbox(
                'Please select the Quarter',
                ('1', '2', '3','4'),key='qgwe2')
    Data_Map_User_df=Data_Aggregated_User_Summary_df.copy()
    top_states=Data_Map_User_df.loc[(Data_Map_User_df['Year'] == int(Year)) & (Data_Map_User_df['Quarter'] ==int(Quarter))]
    top_states_r = top_states.sort_values(by=['Registered_Users'], ascending=False)
    top_states_a = top_states.sort_values(by=['App_Opens'], ascending=False)

    top_states_T=Data_Aggregated_Transaction_df.loc[(Data_Aggregated_Transaction_df['Year'] == int(Year)) & (Data_Aggregated_Transaction_df['Quarter'] ==int(Quarter))]
    topst=top_states_T.groupby('State')
    x=topst.sum().sort_values(by=['Transaction_Count'], ascending=False)
    y=topst.sum().sort_values(by=['Transaction_Amount'], ascending=False)
    # col1, col2, col3, col4= st.columns([2.5,2.5,2.5,2.5])
    tab1, tab3, tab4, tab5 = st.tabs(["Registered Users", "PhonePeApp Openings", "Total Transactions", "Total Amount"])

    with tab1:
        rt=top_states_r[1:10]
        st.markdown("#### :orange[Registered Users :bust_in_silhouette:]")
        st.markdown(rt[[ 'State','Registered_Users']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        fig=px.bar(rt,x="State",y="Registered_Users")
        tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
        with tab1:
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with tab2:
            st.plotly_chart(fig, theme=None, use_container_width=True)

    with tab3:
        at=top_states_a[1:10]
        st.markdown("#### :orange[PhonePeApp Openings:iphone:]")
        st.markdown(at[['State','App_Opens']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
        fig=px.bar(at,x="State",y="App_Opens")
        tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
        with tab1:
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        with tab2:
            st.plotly_chart(fig, theme=None, use_container_width=True)
    with tab4:
        st.markdown("#### :orange[Total Transactions:currency_exchange:]")
        st.write(x[['Transaction_Count']][1:10]) 
    with tab5:
        st.markdown("#### :orange[Total Amount :dollar:]")
        st.write(y['Transaction_Amount'][1:10]) 


     
if select=='Feedback':
    with st.container():
        st.subheader("Hope you enjoyed using this webpage!!!:thumbsup:")
        st.write("Please provide your valuable Feedback!!!:speech_balloon:")
        st.write("##")
        contact_form="""
        <form action="https://formsubmit.co/aravinthvignesh22@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">      
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
        left_column,right_column=st.columns(2)
        with left_column:
            st.markdown(contact_form,unsafe_allow_html=True)