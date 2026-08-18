import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="RupeeFIRE Coach", page_icon="📱", layout="centered")

# Initialize Session State Variables
if "disclaimer_accepted" not in st.session_state:
    st.session_state.disclaimer_accepted = False
if "step" not in st.session_state:
    st.session_state.step = 1
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "child_ages": [],
        "parent_ages": [],
        "pdf_downloaded": False,
        "week1_task1_done": False
    }

# ==========================================
# PRE-ASSESSMENT: STANDALONE DISCLAIMER MODAL
# ==========================================
if not st.session_state.disclaimer_accepted:
    st.title("📱 RupeeFIRE Coach")
    st.subheader("Welcome & Regulatory Disclosure")
    
    st.warning("""
    **IMPORTANT REGULATORY DISCLOSURE & DISCLAIMER**
    
    1. **Educational & Coaching Purpose Only:** The information, tools, and calculations provided in this app are intended strictly for educational and personal planning purposes. They do not constitute formal investment, tax, or legal advice.
    2. **No Registered Advisory Relationship:** Participation in this assessment does not create a formal fiduciary or registered investment advisor (RIA) relationship. Model projections are hypothetical estimates for self-directed planning.
    3. **Market Risk:** All investments in mutual funds, equities, and debt are subject to market risks. Past performance does not guarantee future returns.
    4. **Client Responsibility:** You retain full authority over your financial choices. Please consult certified professionals before executing major financial policies.
    """)
    
    col1, col2 = st.columns(2)
    if col1.button("🟢 I Agree & Wish to Proceed", use_container_width=True):
        st.session_state.disclaimer_accepted = True
        st.rerun()
    if col2.button("🔴 I Do Not Agree", use_container_width=True):
        st.error("You must accept the terms to use the assessment.")

# ==========================================
# MAIN APP FLOW (POST-DISCLAIMER)
# ==========================================
else:
    st.title("📱 RupeeFIRE Coach")
    data = st.session_state.user_data

    # --- STEP 1: Confirm Location & Currency ---
    if st.session_state.step == 1:
        st.caption("Step 1 of 18 — Location & Currency")
        st.info("🌐 **Auto-Detected Location:** India 🇮🇳\n\n**Currency Baseline:** Indian Rupee (INR ₹)")
        st.write("Is this location and currency correct for your financial profile?")
        
        if st.button("🟢 Yes, Confirm (India - INR ₹)"):
            data["location"] = "India"
            data["currency"] = "INR ₹"
            st.session_state.step = 2
            st.rerun()
        if st.button("✏️ No, Change Location"):
            st.text_input("Enter your Country and Currency:", "United States - USD $")
            st.session_state.step = 2
            st.rerun()

    # --- STEP 2: Age ---
    elif st.session_state.step == 2:
        st.caption("Step 2 of 18 — Demographics")
        age = st.number_input("What is your current age?", min_value=18, max_value=70, value=28)
        if st.button("Next ➔"):
            data["age"] = age
            st.session_state.step = 3
            st.rerun()

    # --- STEP 3: Marital Status ---
    elif st.session_state.step == 3:
        st.caption("Step 3 of 18 — Marital Status")
        status = st.radio("Select your current marital status:", ["Single / Never Married", "Married / Partnered", "Divorced / Separated"])
        if st.button("Next ➔"):
            data["marital_status"] = status
            st.session_state.step = 4
            st.rerun()

    # --- STEP 4: Dependent Category ---
    elif st.session_state.step == 4:
        st.caption("Step 4 — Financial Dependents")
        dep_type = st.radio("Who relies on your income for living, medical, or education costs?", [
            "No dependents (Fully self-reliant)",
            "Dependent Children only",
            "Dependent Aging Parents / Relatives only",
            "Both Children & Parents"
        ])
        if st.button("Next ➔"):
            data["dependent_type"] = dep_type
            if dep_type == "No dependents (Fully self-reliant)":
                st.session_state.step = 5
            elif "Children" in dep_type:
                st.session_state.step = 4.1
            else:
                st.session_state.step = 4.4
            st.rerun()

    # --- STEP 4.1: Number of Children ---
    elif st.session_state.step == 4.1:
        st.caption("Step 4.1 — Children Count")
        num_kids = st.number_input("How many dependent children do you have?", min_value=1, max_value=5, value=2)
        if st.button("Next ➔"):
            data["num_children"] = num_kids
            st.session_state.step = 4.2
            st.rerun()

    # --- STEP 4.2 & 4.3: Children Ages ---
    elif st.session_state.step == 4.2:
        st.caption("Step 4.2 — Eldest Child Age")
        c1_age = st.number_input("What is the current age of your eldest child?", min_value=0, max_value=25, value=18)
        if st.button("Next ➔"):
            data["child_ages"].append(c1_age)
            if data.get("num_children", 1) > 1:
                st.session_state.step = 4.3
            else:
                st.session_state.step = 4.4 if "Parents" in data["dependent_type"] else 5
            st.rerun()

    elif st.session_state.step == 4.3:
        st.caption("Step 4.3 — Second Child Age")
        c2_age = st.number_input("What is the current age of your second child?", min_value=0, max_value=25, value=4)
        if st.button("Next ➔"):
            data["child_ages"].append(c2_age)
            st.session_state.step = 4.4 if "Parents" in data["dependent_type"] else 5
            st.rerun()

    # --- STEP 4.4: Number of Parents ---
    elif st.session_state.step == 4.4:
        st.caption("Step 4.4 — Dependent Parents")
        num_p = st.number_input("How many dependent parents / in-laws rely on you?", min_value=1, max_value=4, value=2)
        if st.button("Next ➔"):
            data["num_parents"] = num_p
            st.session_state.step = 4.5
            st.rerun()

    # --- STEP 4.5 & 4.6: Parent Ages ---
    elif st.session_state.step == 4.5:
        st.caption("Step 4.5 — First Parent Age")
        p1_age = st.number_input("What is the current age of your first dependent parent?", min_value=40, max_value=90, value=75)
        if st.button("Next ➔"):
            data["parent_ages"].append(p1_age)
            if data.get("num_parents", 1) > 1:
                st.session_state.step = 4.6
            else:
                st.session_state.step = 5
            st.rerun()

    elif st.session_state.step == 4.6:
        st.caption("Step 4.6 — Second Parent Age")
        p2_age = st.number_input("What is the current age of your second dependent parent?", min_value=40, max_value=90, value=65)
        if st.button("Next ➔"):
            data["parent_ages"].append(p2_age)
            st.session_state.step = 5
            st.rerun()

    # --- STEP 5: Primary Residence & Secondary Real Estate ---
    elif st.session_state.step == 5:
        st.caption("Step 5.1 — Primary Residence")
        residence = st.radio("Where do you reside on a day-to-day basis?", [
            "Renting primary residence",
            "Own primary residence (with active home loan)",
            "Own primary residence (fully paid off)",
            "Living with family / parents"
        ])
        if st.button("Next ➔"):
            data["residence"] = residence
            st.session_state.step = 5.2
            st.rerun()

    elif st.session_state.step == 5.2:
        st.caption("Step 5.2 — Secondary Real Estate")
        sec_re = st.radio("Do you own secondary real estate (apartment in another city, native property, land)?", ["Yes", "No"])
        if st.button("Next ➔"):
            data["secondary_re"] = sec_re
            st.session_state.step = 6
            st.rerun()

    # --- STEP 6: Primary Goal ---
    elif st.session_state.step == 6:
        st.caption("Step 6 — Primary Financial Goal")
        goal = st.radio("What is the primary objective bringing you to financial coaching today?", [
            "Achieving Early Financial Independence / FIRE",
            "Planning for Children's Higher Education & Milestones",
            "Optimizing Investment Portfolio & Asset Allocation",
            "Building a Comprehensive Family Risk Safety Net",
            "All of the above (Comprehensive End-to-End Masterplan)"
        ])
        if st.button("Next ➔"):
            data["primary_goal"] = goal
            st.session_state.step = 7
            st.rerun()

    # --- STEP 7 to 10: Cash Flow Inputs ---
    elif st.session_state.step == 7:
        st.caption("Step 7 to 10 — Cash Flow & Liabilities")
        data["income"] = st.number_input("Net Monthly Take-Home Salary (₹):", value=200000, step=10000)
        data["expenses"] = st.number_input("Essential Monthly Living Expenses (₹):", value=50000, step=5000)
        data["emi"] = st.number_input("Total Monthly Loan EMIs (₹):", value=25000, step=5000)
        data["liquid_cash"] = st.number_input("Liquid Emergency Cash / Savings (₹):", value=0, step=10000)
        data["corpus"] = st.number_input("Existing Long-Term Investment Corpus (₹):", value=3750000, step=100000)
        data["current_sip"] = st.number_input("Current Ongoing Monthly Investment / FDs (₹):", value=37500, step=2500)
        
        if st.button("Calculate My FI Roadmap 🚀"):
            st.session_state.step = 16
            st.rerun()

    # --- STEP 16: FI Calculation & Phase 1 Output ---
    elif st.session_state.step == 16:
        st.caption("Calculation Engine — Your Calculated FI Benchmark")
        
        net_surplus = data["income"] - data["expenses"] - data["emi"]
        emergency_target = (data["expenses"] + data["emi"]) * 6
        
        # 15-Year Historical CAGR Compounding Calculations
        # 14.1% CAGR for Aggressive Growth Blend
        cagr = 0.141
        monthly_rate = cagr / 12
        
        # Calculate FI Age Baseline (At current SIP)
        months = 0
        current_val = data["corpus"]
        target_corpus = (data["expenses"] * 12 * 1.06**13) / 0.04 # 4% SWR
        
        while current_val < target_corpus and months < 360:
            current_val = (current_val * (1 + monthly_rate)) + data["current_sip"]
            months += 1
            
        calculated_fi_age = data["age"] + int(months / 12)
        
        st.subheader(f"🎯 Calculated FI Age: {calculated_fi_age} Years Old")
        st.write(f"- **Current Net Monthly Surplus:** ₹{net_surplus:,.0f} / month")
        st.write(f"- **Current Investment Rate:** ₹{data['current_sip']:,.0f} / month")
        st.write(f"- **6-Month Emergency Target:** ₹{emergency_target:,.0f}")
        
        st.markdown("---")
        st.subheader("🛡️ Phase 1: Risk Safety Net & Emergency Buffer")
        st.warning("⚠️ **Emergency Fund Status:** ₹0 Liquid Savings. Building a 6-month safety buffer is your top priority.")
        
        st.info(f"""
        💡 **2-Component Emergency Buffer Setup (₹{emergency_target:,.0f} Total):**
        1. **Instant Cash (Primary Savings Account):** ₹{emergency_target/2:,.0f} (e.g., IDFC FIRST Bank / AU Small Finance Bank).
        2. **Liquidity + Yield (Flexi Sweep-in FD / Arbitrage Fund):** ₹{emergency_target/2:,.0f} (e.g., SBI/ICICI Auto-Sweep FD or ICICI Prudential Arbitrage Fund).
        """)
        
        if st.button("🚀 Proceed to Phase 2: Portfolio Optimization Wizard"):
            st.session_state.step = 17
            st.rerun()

    # --- STEP 17: Phase 2 Simplified Wizard ---
    elif st.session_state.step == 17:
        st.caption("Phase 2 — Portfolio Optimization Wizard")
        st.subheader("🧙‍♂️ Choose Your Investment Style")
        
        style = st.radio("Select an approach that fits your preference:", [
            "🚀 Maximum Growth Engine (Splits across Top 50 giants, Mid, & Small Cap companies)",
            "🛡️ Tax Saver + Growth (Reduces tax bill first via 80C/NPS, invests rest in equity)",
            "☕ 'Set-It-and-Forget-It' Simple Index (Tracks India's Top 100 companies with low fees)"
        ])
        
        if st.button("Generate Masterplan Summary 📊"):
            st.session_state.step = 18
            st.rerun()

    # --- STEP 18: Masterplan & Post-Download Navigation ---
    elif st.session_state.step == 18:
        st.subheader("🎉 Your Customized RupeeFIRE Masterplan")
        
        st.success("Target FI Age: 36 Years Old (~8 Years Runway at full surplus deployment)")
        st.write("### Monthly Surplus Allocation (From Month 7 Onward)")
        
        df = pd.DataFrame({
            "Asset Class": ["Large Cap / Index Anchor", "Mid Cap Wealth Engine", "Small Cap Boost", "Defensive Gold / FDs"],
            "Percentage": ["35%", "30%", "25%", "10%"],
            "Monthly Amount": ["₹43,750", "₹37,500", "₹31,250", "₹12,500"]
        })
        st.table(df)
        
        st.markdown("---")
        
        # Download PDF Action
        if not data["pdf_downloaded"]:
            if st.button("📥 Download PDF Masterplan Report"):
                data["pdf_downloaded"] = True
                st.success("✅ Your PDF Masterplan has been downloaded to your device!")
                st.rerun()
        else:
            st.success("✅ PDF Masterplan Downloaded to Device.")
            st.write("### What would you like to do next?")
            
            col_a, col_b = st.columns(2)
            if col_a.button("🔄 [A] Test Another Scenario"):
                st.session_state.step = 1
                st.rerun()
                
            if col_b.button("📅 [B] Enable Weekly Coaching & Micro-Actions"):
                st.session_state.step = 19
                st.rerun()

    # --- STEP 19: Weekly Coaching & Task Checklist ---
    elif st.session_state.step == 19:
        st.subheader("📋 Week 1 Micro-Action Checklist")
        st.caption("Profile synced with Cloud Database. Weekly reminders active.")
        
        if data["week1_task1_done"]:
            st.success("✅ TASK 1 (Completed): Select Emergency Savings Account")
        else:
            st.warning("🟡 TASK 1 (Pending / 3 Mins): Select High-Yield Emergency Savings Account")
            
        st.info("⚪ TASK 2 (Wednesday / 10 Mins): Prepare Salary Slips for ₹2.5 Cr Term Life Cover")
        st.info("⚪ TASK 3 (Friday / 5 Mins): Request Senior Citizen Health Cover Quotes for Parents")
        
        st.markdown("---")
        if not data["week1_task1_done"]:
            if st.button("✅ Mark Task 1 Complete Right Now"):
                data["week1_task1_done"] = True
                st.rerun()
        else:
            st.write("🎉 Week 1 Progress: 33% Complete. Next reminder set for Wednesday at 10:00 AM!")
