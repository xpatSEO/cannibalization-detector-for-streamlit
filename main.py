import pandas as pd
import streamlit as st
from helpers import *

# INTERFACE STREAMLIT
def streamlit_main():
    st.set_page_config(layout="wide")
    st.title("Cannibalization detector (v.bêta)")

    with st.sidebar:
        st.title("Instructions (upcoming)")

    # Champ de texte pour saisir les requêtes
    brand_input = st.text_area("Firstly, enter the brands variants (one keyword per line):")
    FILE_LOCATION = st.file_uploader("Then upload your Search Console CSV's export, please name it 'dataset.csv'", ['csv'])

    def job(file_location, brand_variants):
        """
        Main function for the job.
        """
        st.text('-- Start: Creating primary analysis df')
        initial_df = pd.read_csv(file_location)
        non_brand_df = initial_df
        not_empty_spaces = all([brand_variant != '' for brand_variant in brand_variants])
        if brand_variants and not_empty_spaces:
            non_brand_df = remove_brand_queries(initial_df, brand_variants)
        query_page_counts = calculate_query_page_metrics(non_brand_df)
        query_counts = filter_queries_by_clicks_and_pages(query_page_counts)
        wip_df = merge_and_aggregate(query_page_counts, query_counts)
        wip_df = calculate_click_percentage(wip_df)
        wip_df = filter_by_click_percentage(wip_df)
        wip_df = merge_with_page_clicks(wip_df, initial_df)
        wip_df = define_opportunity_levels(wip_df)
        final_df = sort_and_finalize_output(wip_df)
        st.text('-- End: Creating primary analysis df')
        
        st.text('-- Start: Creating supporting dfs')
        qa_df = create_qa_dataframe(initial_df, final_df)
        immediate_opps_df = immediate_opps(final_df)
        instructions_df = create_instructions_df()
        st.text('-- End: Creating supporting dfs')
        
        dict_of_dfs = {
            "instructions": instructions_df, 
            "all_potential_opps": final_df, 
            "high_likelihood_opps": immediate_opps_df,
            "risk_qa_data": qa_df 
        }
        
        st.text('-- Start: Creating excel file')
        create_excel_file(dict_of_dfs, "test")
        st.text('-- End: Creating excel file')
        
        st.text('Job complete!')
        st.subheader("High likelihood opps :")
        st.dataframe(immediate_opps_df)
        st.subheader("Global report :")
        st.dataframe(final_df)

    # Main script execution
    if st.button("Go !"):
        if FILE_LOCATION is not None:
            BRAND_VARIANTS = brand_input.split('\n') if brand_input else []
            if __name__ == "__main__":
                status = job(FILE_LOCATION, BRAND_VARIANTS)
                st.text(status)

streamlit_main()