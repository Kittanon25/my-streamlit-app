import streamlit as st

st.title("🧮 เครื่องคิดเลขอย่างง่าย")

num1 = st.number_input("กรอกตัวเลขที่ 1", value=0.0)
num2 = st.number_input("กรอกตัวเลขที่ 2", value=0.0)

operation = st.selectbox(
    "เลือกเครื่องหมายคำนวณ",
    ("+ (บวก)", "- (ลบ)", "* (คูณ)", "/ (หาร)")
)

if st.button("คำนวณ"):
    result = None
    if operation == "+ (บวก)":
        result = num1 + num2
    elif operation == "- (ลบ)":
        result = num1 - num2
    elif operation == "* (คูณ)":
        result = num1 * num2
    elif operation == "/ (หาร)":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("ไม่สามารถหารด้วย 0 ได้!")

    if result is not None:
        st.success(f"ผลลัพธ์คือ: {result}")