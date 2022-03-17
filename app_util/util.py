import streamlit as st


def check_multiselect_default(session_state_name, options):
    """
    check if all default values are in multiselect options and remove values that are not in options
    (was done because of found streamlit error)
    :param session_state_name: link to default values
    :param options: list of multiselect options
    :return: prechecked default values
    """
    default_value = st.session_state[session_state_name]
    if set(default_value) | set(options) != set(options):
        default_value = set(default_value) & set(options)
    return default_value


def source_filter(sources_list, source_types_list, region_list, state_key_sources, state_key_types, state_key_regions):
    """
    generate common part for filter forms
    :param sources_list: list of all sources in the archive
    :param source_types_list: list of all source types in the archive
    :param region_list: list of all regions in the archive
    :param state_key_sources: link to default sources
    :param state_key_types: link to default source types
    :param state_key_regions: link to default regions
    :return: chosen sources, source types and regions
    """
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
