@@ -4,11 +4,11 @@
df_top10_number = pd.read_csv('./data/6ko_top10_number.csv')
df_top10_minutes = pd.read_csv('./data/6ko_top10_minutes.csv')

#def display():
col1, col2 = st.columns(2)
with col1:
    st.header("Top 10 in number of media translated")
    st.dataframe(df_top10_number)
with col2:
    st.header("Top 10 in number of minutes translated")
    st.dataframe(df_top10_minutes)
def display_international():
    col1, col2 = st.columns(2)
    with col1:
        st.header("Top 10 in number of media translated")
        st.dataframe(df_top10_number)
    with col2:
        st.header("Top 10 in number of minutes translated")
        st.dataframe(df_top10_minutes)