import streamlit as st


def check_multiselect_default(session_state_name, options):
    default_value = st.session_state[session_state_name]
    if set(default_value) | set(options) != set(options):
        default_value = set(default_value) & set(options)
    return default_value


def source_filter(sources_list, source_types_list, region_list, state_key_sources, state_key_types, state_key_regions):
    if "" in region_list:
        region_list.remove("")
    if "Россия" in region_list:
        region_list.remove("Россия")
    if "Федеральные источники" not in region_list:
        region_list.append("Федеральные источники")
    sources_default = check_multiselect_default(state_key_sources, sources_list)
    sources = st.multiselect('Выберите источники по названию',
                             sources_list,
                             default=sources_default)
    sources_types_default = check_multiselect_default(state_key_types, source_types_list)
    source_types = st.multiselect('Или по типу источника...',
                                  source_types_list,
                                  default=sources_types_default)
    regions_default = check_multiselect_default(state_key_regions, region_list)
    regions = st.multiselect('...и региону',
                             region_list,
                             default=regions_default)
    return sources, source_types, regions
