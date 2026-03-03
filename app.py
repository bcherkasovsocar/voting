import streamlit as st
from streamlit_sortables import sort_items

st.set_page_config(page_title="Drag & Drop Voting", layout="wide")
st.title("🗳️ Drag candidates into bins")

# ---- Demo data ----
CANDIDATES = ["Thomas", "Boris", "Eric", "Nisha, "Carlo", "Sohaib", "Javeed", "Moritz"]

# ---- Simple session “database” (per user session) ----
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "last_vote" not in st.session_state:
    st.session_state.last_vote = None  # {"Gay": [...], "Not Gay": [...]}
if "bins" not in st.session_state:
    st.session_state.bins = [
        {"header": "Gay", "items": CANDIDATES.copy()},
        {"header": "Not Gay", "items": []},
    ]

st.caption("Drag names into **Gay** or **Not Gay**. Then submit to lock in your vote.")

# left, right = st.columns(2)

# with left:
#     st.subheader("Gay")
# with right:
#     st.subheader("Not Gay")

# streamlit-sortables supports multiple containers by passing a dict of lists
# Start with everyone in Bin A (or create a 3rd “Unassigned” bin if you prefer)

# Optional: lock dragging after submit
disabled = st.session_state.submitted

bins = sort_items(
    st.session_state.bins,
    direction="vertical",   # "vertical" also works
    multi_containers=True,
    key="vote_bins",
)

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("Submit vote ✅", disabled=disabled):
        st.session_state.submitted = True
        st.session_state.last_vote = bins
        st.toast("Vote submitted!")

with col2:
    if st.button("Reset ↩️"):
        st.session_state.submitted = False
        st.session_state.last_vote = {"Gay": CANDIDATES.copy(), "Not Gay": []}
        st.rerun()

with col3:
    st.write("")

st.divider()

# ---- Results ----
st.subheader("Results")
if st.session_state.submitted:
    bin_a = bins[0]["items"]
    bin_b = bins[1]["items"]

    st.write(f"{len(bin_a)} Gay people around..watch your back!")
    st.write(f"{len(bin_b)} Not Gay people you can trust")
    st.write("Fun fact: Moritz thinks you're gay!")
