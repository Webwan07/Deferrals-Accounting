import streamlit as st
from datetime import datetime, date

st.set_page_config("Deferrals Accounting",layout='centered',initial_sidebar_state='auto',)

current_year_int = int(datetime.now().year)
default_date = date(current_year_int, 12, 31)

sidebar_option = [["Pre-payments","Pre-collection"],
                  ["Asset Method","Expense Method"],
                  ["Liability Method","Income Method"]]

class Equation:
    def __init__(self,account):
        self.name = account

    def debit(*num):
        return num[0] + num[1]
    
    def credit(*num):
        return num[0] - num[1]

def under_development_info():
    st.info("Under Development!")

def hide_footer():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style,unsafe_allow_html=True)

def get_date():
    try:
        col1,col2 = st.columns(2)
        with col1:
            x = st.date_input('Current date',key='current')
        with col2:
            y = st.date_input('Adjusting date',key='end',value=default_date)
        x,y = str(x),str(y)
    
        x_d = [int(p_d) for p_d in x.split('-')]
        y_d = [int(p_d) for p_d in y.split('-')]
        return [[x_d[1],x_d[2],x_d[0]],[y_d[1],y_d[2],y_d[0]]]
    except ValueError as e:
        print(e)

def get_account_amount(*string):
    step = []
    col1, col2 = st.columns(2)
    with col1:
        step.append(st.text_input("Debit",key='debit_k',value=string[0]).capitalize())
        step.append(st.text_input("Credit",key='credit_k',value=string[1]).capitalize())
    with col2:
        step.append(st.number_input("Amount",key='debit_a'))
        step.append(st.number_input("Amount",key='credit_a'))
    
    return step

def deferrals_equation(amount,c_y, e_y):
    g_y = (e_y[2] - c_y[2]) + 1
    g_y *= 12

    if c_y[1] > 15:
        g_m = 12 - c_y[0]
    else:
        g_m = 12 - (c_y[0]-1)

    used = g_m
    unused = g_y - g_m
    org_a = amount
    amount /= g_y
    used_a = amount * used
    unused_a = amount * unused
    print(f"get amount{amount}")
    print(f"USED: {used} : {used_a}\nUNUSED: {unused} : {unused_a}")
    return [[used,used_a],[unused,unused_a],amount]

def get_words(a):
    the_word = a.split()

    get_word = the_word.index("Prepaid")

    if get_word < len(the_word) - 1:
        next_word = the_word[get_word + 1]
    else:
        next_word = None
    return next_word

def asset_method(*s):
    equation = Equation("Asset")
    st.header("Initial entry")
    try:
        a = get_account_amount(s[1],s[2])
        tab1,tab2 = st.tabs(["Date method #1","Date method #2"])
        with tab1:
            b = get_date()
        with tab2:
            under_development_info()

        print(f"a and B: {a} {a[1]}: {b} {a[2]}")
        if st.button("Submit",key='asset-btn'):
            if a[2] != 0 and a[3] != 0 and a[2] == a[3]:
                if a[0].strip().startswith("Prepaid ") and a[1].strip().startswith("Cash on "):
                    print(f"a: {a}")
                    print(f"Amount: {a[2]} : {b[0]} : {b[1]}")
                    result = deferrals_equation(a[2],b[0],b[1])
                    print(f"Result: {result}")

                    pre = [["Expense","Used","Prepaid","Unused"],
                                [0,0+result[0][1],"Increase","Debit"],
                                [result[0][1]+result[1][1],
                                (result[1][1]+result[0][1])-result[1][1],"Decrease","Credit"]]
                    st.write("---")
                    st.header("Solution")

                    a_data = {" ": [pre[0][0],pre[0][2]," "],
                            "  ":[pre[0][1],pre[0][3]," "],
                            "Months":[result[0][0],result[1][0],12],
                            "   ":[f"{result[0][0]} x {result[2]} = ",f"{result[1][0]} x {result[2]} = "," "],
                            "Should be":[result[0][1],result[1][1]," "],
                            "Recorded":[0,result[0][1]+result[1][1]," "],
                            "    ":[f"{0} + {result[0][1]} = ",\
                                    f"({result[0][1]} + {result[1][1]}) - {result[1][1]} = ", " "],
                            "Adjusting":[0+result[0][1],(result[0][1]+result[1][1])-result[1][1]," "],
                            "     ":["↑ Debit","↓ Credit"," "]}
                    
                    st.experimental_data_editor(a_data)

                    st.write("---")

                    get_word = get_words(a[0]).capitalize()
                    debit = f"{get_word} Expense"
                    credit = f"Prepaid {get_word}"

                    debit_a = 0+result[0][1]
                    credit_a = (result[1][1]+result[0][1])-result[1][1]

                    pre_adj = [[debit,debit_a],[credit,credit_a]]
                    print(f"The word: {pre_adj}")
                    adjusting_d = {" ":[f"12/31/{b[0][2]}"," "],
                                   "  ":[debit,credit],
                                   "   ":[f"$ {debit_a}",f"$ {credit_a}"]}
                    st.header("Adjusting entry")
                    st.experimental_data_editor(adjusting_d)
                else:
                    st.error("Invalid Account Name!")
            else:
                if not(a[2] != 0 and a[3] != 0 and a[2] == a[3]) and \
                    not (a[0].strip().startswith("Prepaid ") and a[1].strip().startswith("Cash on ")):
                    st.error("Invalid Account Name!")
                    st.warning(f"Invalid amount: {a[2]} & {a[3]}")
                else:
                    st.warning(f"Invalid amount: {a[2]} & {a[3]}")
    except TypeError as w:
        print(w)
    except ValueError as a:
        print(a)
    except st.errors.StreamlitAPIException as n:
        print(n)

def expense_method():
    pass

def liability_method():
    pass

def income_mothod():
    pass

def sidebar_section():
    step = []
    with st.sidebar:
        step.append(st.selectbox("Choose",options=sidebar_option[0]))
        st.json({"Created by":{"Name":"Josuan Leonardo S. Hulom",
                               "Course&Year":"BSIT 1",
                               "Department":"College of Computer Studies",
                               "College":"Cebu Roosevelt Memorial College"}})
    return step

def main():
    try:
        main_step = []
        get_sidebar = sidebar_section()
        print(get_sidebar)

        if get_sidebar[0] == sidebar_option[0][0]:
            st.title(sidebar_option[0][0])
            col1, col2 = st.columns(2)
            with col1:
                st.json({"Asset Method":{"Initial entry":{"Initial date":"(Appropriate) Expense xxx",\
                                                        " ":"Cash (Appropriate) xxx"},\
                                        "Adjusting entry":{"Adjusting date":"(Appropriate) Expense xxx",\
                                                            "  ":"Prepaid (Appropriate) xxx"}}})
            with col2:
                st.json({"Expense Method":{"Initial entry":{"Initial date":"Prepaid (Appropriate) xxx",\
                                                        " ":"Cash (Appropriate) xxx"},\
                                        "Adjusting entry":{"Adjusting date":"Prepaid (Appropriate) xxx",\
                                                            "  ":"(Appropriate) Expense xxx"}}})
            tab1,tab2 = st.tabs([sidebar_option[1][0],sidebar_option[1][1]])
            st.write("---")
            with tab1:
                main_step.append(asset_method("$","Prepaid","Cash on"))
            with tab2:
                st.subheader(sidebar_option[1][1])
                under_development_info()
        elif get_sidebar[0] == sidebar_option[0][1]:
            st.subheader(sidebar_option[0][1])
            tab1,tab2 = st.tabs([sidebar_option[2][0],sidebar_option[2][1]])
            with tab1:
                under_development_info()
            with tab2:
                under_development_info()
    except TypeError as t:
        print(f"Error: {t}")
        
    hide_footer()

if __name__ == '__main__':
    main()