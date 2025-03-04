import streamlit as st
import matplotlib.pyplot as plt
import preprocessor,helper
import seaborn as sns
st.sidebar.title("whatsapp chat analyzers")
import streamlit as st
import pandas as pd
#from io import StringIO
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #as this is a binary data to convert this data in to string we use
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    # fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("show analysis"):
        total_message,words,num_media_message,links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Exchange")
            st.title(num_media_message)
        with col4:
            st.header("Total links Shared")
            st.title(links)
        #finding the busiest user in the group(Group Level)
        if selected_user=='overall':
            st.title('Most Busy User')
            x,new_df= helper.most_buy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        st.subheader('Commonly used word cloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        st.subheader('Frequency of Common words')
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.header('Most Used Emojis')
        col1,col2=st.columns(2)
        emoji_df=helper.cnt_emoji(selected_user,df)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
