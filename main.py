import streamlit as st
import pandas as pd
import altair as alt
import time
import random
import emojis as em
from ALL_algo import bubble_sort, insertion_sort, merge_sort, quick_sort, heap_sort, bucket_sort, radix_sort, counting_sort, k_smallest

def format_array(arr):
    html_arr = "<div style='overflow-x: auto;'><table style='border-collapse: collapse;'><tr>"
    for item in arr:
        html_arr += f"<td style='border: 1px solid black; padding: 5px;'>{item}</td>"
    html_arr += "</tr></table></div>"
    return html_arr

def execute_algorithm(algo, arr, k=None):
    start_time = time.perf_counter()
    steps = []

    if algo == k_smallest:
        if k is not None and 0 < k <= len(arr):
            result = algo(arr.copy(), 0, len(arr) - 1, k)
            steps.append(result)
        else:
            steps.append("Invalid value of k.")
    else:
        for step in algo(arr.copy()):
            steps.append(step.copy())

    end_time = time.perf_counter()
    exec_time_microseconds = (end_time - start_time) * 1_000_000
    return steps, exec_time_microseconds

def main():
    if 'arr' not in st.session_state:
        st.session_state.arr = []

    st.markdown("<h1 style='text-align: center; color: red;'>Sorting Analyzer</h1>", unsafe_allow_html=True)
    random_array = st.checkbox('Generate random array')

    if random_array:
        arr_size = st.slider('Array size', 5, 100, 10)
        if not st.session_state.arr or st.button('Generate New Array'):
            st.session_state.arr = random.sample(range(1, 1000), arr_size)
        st.markdown("Generated Unsorted Array:")
        st.markdown(format_array(st.session_state.arr), unsafe_allow_html=True)
    else:
        arr_str = st.text_input("Enter comma-separated elements of the array:", '')
        if arr_str:
            try:
                st.session_state.arr = [int(item) for item in arr_str.split(',')]
            except ValueError:
                st.error("Please enter a valid comma-separated list of integers.")

    selected_algos = st.multiselect('Select algorithms to compare', 
                                    ['Insertion Sort', 'Bubble Sort', 'Merge Sort', 'Quick Sort', 
                                     'Heap Sort', 'Bucket Sort', 'Radix Sort', 'Counting Sort', 'K Smallest'], 
                                    default=['Insertion Sort'])
    k_value = None
    if 'K Smallest' in selected_algos:
        k_value = st.number_input('Enter the value of k for K Smallest Algorithm', 
                                  min_value=1, max_value=len(st.session_state.arr), value=1)

    if st.button('Compare Performance'):
        algo_functions = {'Insertion Sort': insertion_sort, 'Bubble Sort': bubble_sort, 'Merge Sort': merge_sort, 'Quick Sort': quick_sort,
                          'Heap Sort': heap_sort, 'Bucket Sort': bucket_sort, 'Radix Sort': radix_sort, 'Counting Sort': counting_sort, 'K Smallest': k_smallest}
        times = {}
        for algo in selected_algos:
            original_arr = st.session_state.arr.copy()
            if algo == 'K Smallest':
                steps, exec_time_microseconds = execute_algorithm(algo_functions[algo], original_arr, k_value)
            else:
                steps, exec_time_microseconds = execute_algorithm(algo_functions[algo], original_arr)
            times[algo] = exec_time_microseconds

            with st.expander(f"{algo} Output and Performance"):
                st.write(f"Execution Time: {exec_time_microseconds:.2f} microseconds")
                steps_text = ""
                for i, step in enumerate(steps):
                    step_str = ', '.join(map(str, step)) if isinstance(step, list) else str(step)
                    steps_text += f"**Step {i+1}:** {step_str}\n\n"
                st.text_area("Sorting Steps:", steps_text, height=300)

        df_times = pd.DataFrame(list(times.items()), columns=['Algorithm', 'Execution Time (microseconds)'])
        bar_chart = alt.Chart(df_times).mark_bar().encode(
            x=alt.X('Algorithm', title='Sorting Algorithm'),
            y=alt.Y('Execution Time (microseconds)', title='Execution Time (Microseconds)'),
            color=alt.Color('Algorithm', legend=None),
            tooltip=['Algorithm', 'Execution Time (microseconds)']
        ).interactive()
        st.markdown(f"<h3 style='text-align: center;'><i>Time Taken:</i>{em.encode(':timer_clock:')}</h3>", unsafe_allow_html=True)
        st.altair_chart(bar_chart, use_container_width=True)

if __name__ == '__main__':
    main()
