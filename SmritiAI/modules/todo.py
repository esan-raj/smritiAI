import streamlit as st

# To-Do List function
def todo_app():
    st.title("📝 To-Do List")

    # Initialize session state for tasks
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    # Add a new task
    new_task = st.text_input("Add a new task:")
    if st.button("➕ Add Task"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})
            st.success("Task added!")

    # Show the task list
    st.write("### Your Tasks:")
    for index, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.write(f"✅ {task['task']}" if task["done"] else f"🔲 {task['task']}")
        with col2:
            if st.button("✔️", key=f"done_{index}"):
                st.session_state.tasks[index]["done"] = True

    # Clear completed tasks
    if st.button("🗑️ Clear Completed Tasks"):
        st.session_state.tasks = [task for task in st.session_state.tasks if not task["done"]]
        st.success("Completed tasks removed!")
