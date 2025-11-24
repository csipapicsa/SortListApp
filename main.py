import streamlit as st
import re

def on_change_output():
    try:
        del st.session_state['output']
    except:
        pass

st.set_page_config(page_title="List Sorter", page_icon="📝")

st.title("Simple List Sorter")
st.markdown("Paste your messy list, get it sorted. Dead simple.")

# Create two columns for input and output
col1, col2 = st.columns(2)

with col1:
    user_input = st.text_area(
        "Input List",
        height=400,
        placeholder="Paste your list here...\nCan be separated by commas, semicolons, new lines, whatever",
        key="input"
    )

    print("user_input:", user_input)

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    
    # Separator selection
    separator_option = st.radio(
        "Split by:",
        ["Auto-detect", "Comma", "Semicolon", "New line", "Space", "Custom"]
    )
    
    custom_separator = ""
    if separator_option == "Custom":
        custom_separator = st.text_input("Enter custom separator:", value=",")
    
    # Case sensitivity
    case_sensitive = st.checkbox("Case sensitive sorting", value=False)
    
    # Sort order
    ascending = st.radio(
        "Sort order:",
        ["Ascending (A→Z)", "Descending (Z→A)"]
    ) == "Ascending (A→Z)"
    
    # Additional options
    st.markdown("---")
    remove_empty = st.checkbox("Remove empty items", value=True)
    remove_duplicates = st.checkbox("Remove duplicates", value=False)
    result_seperator = st.toggle(" Comma or new line? ")
    # trim_spaces = st.checkbox("Trim whitespace", value=True)

# Add Sort button
sort_button = st.button("🔄 Sort List", type="primary", on_click=on_change_output)

# Process the list
with col2:
    if sort_button and user_input: 
        sorted_items = None
        # Determine separator
        if separator_option == "Auto-detect":
            # Try to detect the most likely separator
            if '\n' in user_input and (user_input.count('\n') > user_input.count(',')):
                items = user_input.split('\n')
            elif ',' in user_input:
                items = re.split('[,;]', user_input)  # Split by comma or semicolon
            elif ';' in user_input:
                items = user_input.split(';')
            else:
                items = user_input.split()  # Default to space
        elif separator_option == "Comma":
            items = user_input.split(',')
        elif separator_option == "Semicolon":
            items = user_input.split(';')
        elif separator_option == "New line":
            items = user_input.split('\n')
        elif separator_option == "Space":
            items = user_input.split(' ')
        elif separator_option == "Custom" and custom_separator:
            items = user_input.split(custom_separator)
        else:
            items = [user_input]
        
        # Clean up items
        # if trim_spaces:
        items = [item.strip() for item in items]
        
        if remove_empty:
            items = [item for item in items if item]
        
        if remove_duplicates:
            # Preserve order while removing duplicates
            seen = set()
            unique_items = []
            for item in items:
                if item.lower() not in seen:
                    seen.add(item.lower())
                    unique_items.append(item)
            items = unique_items
        
        # Sort the items
        if items:
            sorted_items = sorted(
                items,
                key=lambda x: x if case_sensitive else x.lower(),
                reverse=not ascending
            )
            
            # Store in session state
            st.session_state['sorted_result'] = sorted_items
    
    # Display results if they exist in session state
    if 'sorted_result' in st.session_state and st.session_state['sorted_result']:
        sorted_items = st.session_state['sorted_result']

        if result_seperator:
            result = '\n'.join(sorted_items)
        else:
            result = ', '.join(sorted_items)
            
        # Display result
        result = st.text_area(
            "Sorted Result",
            value=result,
            height=400
        )
        
        # Quick stats
        st.caption(f"📊 {len(sorted_items)} items sorted")
        
        # Copy buttons for different formats
        st.markdown("**Quick export:**")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("Copy as CSV"):
                st.code(', '.join(sorted_items))
        with col_b:
            if st.button("Copy with semicolons"):
                st.code('; '.join(sorted_items))
        with col_c:
            if st.button("Copy quoted"):
                st.code(', '.join([f'"{item}"' for item in sorted_items]))
    else:
        st.text_area(
            "Sorted Result",
            value="",
            height=400,
            placeholder="Sorted list will appear here after clicking Sort...",
            key="output_placeholder"
        )

# Footer
st.markdown("---")
st.markdown("*Paste any messy list → Get it sorted → Copy and go*")