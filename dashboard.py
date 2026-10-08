import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FSD Advisor Directory",
    page_icon="📊",
    layout="wide",
)

DATA_FILE = "Submission File (Gunjan)_SUBMISSION.xlsx"
SHEET_NAME = "FSD directory"


@st.cache_data
def load_data():
    df = pd.read_excel(
        DATA_FILE,
        sheet_name=SHEET_NAME,
        header=1,
        dtype=str,
    )

    df = df.fillna("")

    df = df.rename(columns={
        "profile url": "profile_url",
        "scraped by": "scraped_by",
    })

    return df


df = load_data()


# Header

st.title("FSD Advisor Directory")
st.caption("United States Financial Advisor Directory")

st.divider()


# Sidebar filters

st.sidebar.header("Filters")


def options(column):
    values = sorted(
        v for v in df[column].dropna().unique()
        if str(v).strip()
    )
    return ["All"] + values


country = st.sidebar.selectbox(
    "Country",
    options("country"),
)

state = st.sidebar.selectbox(
    "State",
    options("state"),
)

city = st.sidebar.selectbox(
    "City",
    options("city"),
)

zip_code = st.sidebar.selectbox(
    "ZIP",
    options("zip"),
)

website_filter = st.sidebar.selectbox(
    "Website",
    ["All", "Yes", "No"],
)

linkedin_filter = st.sidebar.selectbox(
    "LinkedIn",
    ["All", "Yes", "No"],
)

facebook_filter = st.sidebar.selectbox(
    "Facebook",
    ["All", "Yes", "No"],
)


# Apply filters

filtered = df.copy()

if country != "All":
    filtered = filtered[filtered["country"] == country]

if state != "All":
    filtered = filtered[filtered["state"] == state]

if city != "All":
    filtered = filtered[filtered["city"] == city]

if zip_code != "All":
    filtered = filtered[filtered["zip"] == zip_code]


def apply_presence_filter(data, column, choice):
    if choice == "Yes":
        return data[data[column].str.strip() != ""]
    elif choice == "No":
        return data[data[column].str.strip() == ""]
    return data


filtered = apply_presence_filter(
    filtered,
    "website",
    website_filter,
)

filtered = apply_presence_filter(
    filtered,
    "linkedin",
    linkedin_filter,
)

filtered = apply_presence_filter(
    filtered,
    "facebook",
    facebook_filter,
)


# KPIs

total_firms = len(df)
filtered_count = len(filtered)

unique_states = (
    filtered["state"]
    .replace("", pd.NA)
    .nunique()
)

unique_cities = (
    filtered["city"]
    .replace("", pd.NA)
    .nunique()
)

unique_zips = (
    filtered["zip"]
    .replace("", pd.NA)
    .nunique()
)

firms_with_website = (
    filtered["website"].str.strip() != ""
).sum()

firms_with_linkedin = (
    filtered["linkedin"].str.strip() != ""
).sum()

firms_with_facebook = (
    filtered["facebook"].str.strip() != ""
).sum()


st.subheader("Directory Overview")


k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Total Advisor Firms",
    f"{total_firms:,}",
)

k2.metric(
    "Filtered Advisor Count",
    f"{filtered_count:,}",
)

k3.metric(
    "Unique States",
    f"{unique_states:,}",
)

k4.metric(
    "Unique Cities",
    f"{unique_cities:,}",
)


k5, k6, k7, k8 = st.columns(4)

k5.metric(
    "Unique ZIP Codes",
    f"{unique_zips:,}",
)

k6.metric(
    "Firms with Website",
    f"{firms_with_website:,}",
)

k7.metric(
    "Firms with LinkedIn",
    f"{firms_with_linkedin:,}",
)

k8.metric(
    "Firms with Facebook",
    f"{firms_with_facebook:,}",
)


st.divider()


# Detailed table

st.subheader("Advisor Directory")

display_df = filtered.copy()


# These fields are not present in the Part 1 source,
# so they remain blank.

display_df["CRD Number"] = ""
display_df["Email Address"] = ""
display_df["Minimum Investable Assets"] = ""

display_df["Firm Name"] = display_df["firm"]

display_df["Address"] = (
    display_df["street_address"]
    .fillna("")
    .str.strip()
)

display_df["City"] = display_df["city"]
display_df["State"] = display_df["state"]
display_df["ZIP Code"] = display_df["zip"]
display_df["Phone Number"] = display_df["phone"]
display_df["Website URL"] = display_df["website"]
display_df["LinkedIn URL"] = display_df["linkedin"]
display_df["Facebook URL"] = display_df["facebook"]


table_columns = [
    "Firm Name",
    "CRD Number",
    "Address",
    "City",
    "State",
    "ZIP Code",
    "Phone Number",
    "Email Address",
    "Website URL",
    "LinkedIn URL",
    "Facebook URL",
    "Minimum Investable Assets",
]


display_df = display_df[table_columns]


st.dataframe(
    display_df,
    width="stretch",
    height=600,
    hide_index=True,
    column_config={
        "Website URL": st.column_config.LinkColumn(
            "Website URL",
        ),
        "LinkedIn URL": st.column_config.LinkColumn(
            "LinkedIn URL",
        ),
        "Facebook URL": st.column_config.LinkColumn(
            "Facebook URL",
        ),
    },
)


st.caption(
    f"Showing {len(display_df):,} advisor records after applying filters."
)
