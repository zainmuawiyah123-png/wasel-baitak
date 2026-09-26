import sqlite3
import streamlit as str_app
import urllib.parse

DB_NAME = "wasel_baitak_pro_final.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # إعادة إنشاء الجداول نظيفة لضمان تحميل المتاجر والمنتجات بالصور المخصصة بدقة
    c.execute("DROP TABLE IF EXISTS stores")
    c.execute("DROP TABLE IF EXISTS products")
    c.execute("DROP TABLE IF EXISTS customers")
    c.execute("DROP TABLE IF EXISTS orders")
    c.execute("DROP TABLE IF EXISTS drivers")
    c.execute("DROP TABLE IF EXISTS vendors")
    
    c.execute("""
        CREATE TABLE customers (
            phone TEXT PRIMARY KEY,
            name TEXT,
            address TEXT,
            location TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE stores (
            name TEXT PRIMARY KEY, 
            category TEXT, 
            phone TEXT, 
            location TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT, 
            category TEXT, 
            item_name TEXT, 
            price REAL, 
            unit_type TEXT,
            image_url TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            customer_phone TEXT,
            customer_address TEXT,
            store_name TEXT,
            items_desc TEXT,
            sub_total REAL DEFAULT 0.0,
            delivery_fee REAL DEFAULT 1.50,
            service_fee REAL DEFAULT 0.25,
            grand_total REAL,
            payment_method TEXT,
            order_status TEXT,
            assigned_driver TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, 
            phone TEXT, 
            vehicle_type TEXT,
            status TEXT DEFAULT 'متوفر'
        )
    """)
    
    c.execute("""
        CREATE TABLE vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, 
            phone TEXT, 
            store_name TEXT
        )
    """)
    
    # إدخال المتاجر الأساسية
    default_stores = [
        ("التموين المركزي", "مواد تموينية", "0791234567", "الكرك - الوسط التجاري"),
        ("ملاحم الكرك البلدية", "لحوم", "0792345678", "الكرك - السوق القديم"),
        ("خضار وفواكه الدلتا", "خضار وفواكه", "0793456789", "الكرك - الحارة الشرقية"),
        ("مطاعم قلعة الكرك", "مطاعم", "0794567890", "الكرك - الممشى"),
        ("حلويات السعادة", "حلويات", "0795678901", "الكرك - المرج"),
        ("مكسرات المحطة", "مكسرات", "0796789012", "الكرك - الثنية"),
        ("صيدلية الدواء الشامل", "صيدليات", "0797890123", "الكرك - شارع المستشفى")
    ]
    c.executemany("INSERT INTO stores (name, category, phone, location) VALUES (?, ?, ?, ?)", default_stores)
    
    # المنتجات مع صور دقيقة لكل صنف (باكيتات، أكياس، وعبوات حقيقية)
    default_products = [
        ("التموين المركزي", "مواد تموينية", "سكر الأسرة الأبيض الناعم (5 كغ)", 3.75, "باكيت / كيس", "https://images.unsplash.com/photo-1581441363689-1f3c3c342617?w=300"),
        ("التموين المركزي", "مواد تموينية", "بن تركي العميد هيل وسط (باكيت/علبة)", 8.50, "كيلو", "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=300"),
        ("التموين المركزي", "مواد تموينية", "شاي الربيع فرط الفاخر (باكيت)", 4.20, "باكيت", "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=300"),
        ("التموين المركزي", "مواد تموينية", "سمنة بلدي أصلي غنم وبقر", 6.50, "كيلو", "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=300"),
        ("التموين المركزي", "مواد تموينية", "زيت ذرة عافية (1.5 لتر)", 3.80, "جلن / حبة", "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300"),
        ("التموين المركزي", "مواد تموينية", "أرز المصري زعتري الفاخر", 1.80, "كيلو", "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300"),
        ("ملاحم الكرك البلدية", "لحوم", "لحم عجل بلدي تازه", 9.50, "كيلو", "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=300"),
        ("ملاحم الكرك البلدية", "لحوم", "دجاج طازج نظيف كامل", 2.30, "كيلو", "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=300"),
        ("خضار وفواكه الدلتا", "خضار وفواكه", "بندورة بلدي حمراء", 0.50, "كيلو", "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300"),
        ("خضار وفواكه الدلتا", "خضار وفواكه", "خيار طازج", 0.60, "كيلو", "https://images.unsplash.com/photo-1449300079321-c0e9241f9851?w=300"),
        ("خضار وفواكه الدلتا", "خضار وفواكه", "موز استوائي طازج", 1.25, "كيلو", "https://images.unsplash.com/photo-1543218024-57a4014d4e3b?w=300"),
        ("مطاعم قلعة الكرك", "مطاعم", "سدر منسف اردني بالجميد الكركي", 12.00, "وجبة / سدر", "https://images.unsplash.com/photo-1544025162-d76694265947?w=300"),
        ("مطاعم قلعة الكرك", "مطاعم", "برغر لحم دبل سبشل", 4.50, "وجبة", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300"),
        ("حلويات السعادة", "حلويات", "كنافة نابلسية خشنة بالجبنة", 5.00, "كيلو", "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=300"),
        ("صيدلية الدواء الشامل", "صيدليات", "بنادول بلس (Panadol)", 1.85, "باكيت", "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300")
    ]
    c.executemany("INSERT INTO products (store_name, category, item_name, price, unit_type, image_url) VALUES (?, ?, ?, ?, ?, ?)", default_products)

    c.execute("INSERT OR IGNORE INTO drivers (id, name, phone, vehicle_type, status) VALUES (1, 'خالد السائق', '0799999999', 'سكوتر توصيل', 'متوفر')")
    c.execute("INSERT OR IGNORE INTO vendors (id, name, phone, store_name) VALUES (1, 'أحمد البائع', '0798888888', 'التموين المركزي')")

    conn.commit()
    conn.close()

init_db()

str_app.set_page_config(page_title="منصة واصل بيتك - نظام الطلبات الذكي", layout="wide", page_icon="🛵")

str_app.sidebar.title("🛵 منصة واصل بيتك")
str_app.sidebar.markdown("---")
portal = str_app.sidebar.radio("اختر البوابة:", [
    "🛒 بوابة الزبائن (الرئيسية)", 
    "🔔 لوحة الإدارة المركزية",
    "🏪 بوابة البائعين والمتاجر",
    "🛵 بوابة السائقين للتوصيل"
])

conn = get_db_connection()
c = conn.cursor()

# ==========================================
# 1. بوابة الزبائن
# ==========================================
if portal == "🛒 بوابة الزبائن (الرئيسية)":
    str_app.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🛒 منصة واصل بيتك - طلباتك أسرع لبيتك</h1>", unsafe_allow_html=True)
    
    if "customer_logged_in" not in str_app.session_state:
        str_app.session_state.customer_logged_in = False
        str_app.session_state.cust_phone = ""
        str_app.session_state.cust_name = ""
        str_app.session_state.cust_address = ""

    if not str_app.session_state.customer_logged_in:
        str_app.info("👋 أهلاً بك! يرجى إدخال بياناتك لمرة واحدة لنبدأ طلباتك الفورية:")
        with str_app.form("reg_form"):
            r_name = str_app.text_input("الاسم الكريم:")
            r_phone = str_app.text_input("رقم الهاتف:")
            r_address = str_app.text_input("عنوان التوصيل بالتفصيل (المدينة، الحي، الشارع):")
            r_location = str_app.text_input("رابط موقع اللوكيشن (Google Maps link - اختياري):")
            submit_reg = str_app.form_submit_button("حفظ الدخول وبدء التسوق")
            
            if submit_reg:
                if r_name.strip() and r_phone.strip() and r_address.strip():
                    c.execute("INSERT OR REPLACE INTO customers (phone, name, address, location) VALUES (?, ?, ?, ?)", 
                              (r_phone.strip(), r_name.strip(), r_address.strip(), r_location.strip()))
                    conn.commit()
                    str_app.session_state.customer_logged_in = True
                    str_app.session_state.cust_phone = r_phone.strip()
                    str_app.session_state.cust_name = r_name.strip()
                    str_app.session_state.cust_address = r_address.strip()
                    str_app.success("تم الدخول بنجاح!")
                    str_app.rerun()
                else:
                    str_app.error("الرجاء تعبئة الاسم ورقم الهاتف والعنوان.")
    else:
        str_app.success(f"أهلاً بك يا **{str_app.session_state.cust_name}** | هاتف: {str_app.session_state.cust_phone} | العنوان: {str_app.session_state.cust_address}")
        if str_app.button("تسجيل خروج / تبديل الحساب"):
            str_app.session_state.customer_logged_in = False
            str_app.rerun()

        str_app.markdown("---")
        
        str_app.markdown("### 🔍 البحث السريع عن الأصناف")
        search_kw = str_app.text_input("ابحث عن أي مادة (سكر، قهوة، شاي، منسف...):", placeholder="اكتب ما تبحث عنه...")
        if search_kw.strip():
            str_app.markdown(f"#### نتائج البحث عن: `{search_kw}`")
            c.execute("SELECT store_name, item_name, price, unit_type, image_url FROM products WHERE item_name LIKE ?", (f"%{search_kw.strip()}%",))
            res = c.fetchall()
            if not res:
                str_app.info("عذراً، لم نجد صنفاً مطابَقاً لبحثك.")
            else:
                for r_st, r_item, r_pr, r_un, r_img in res:
                    col_img, col_txt = str_app.columns([1, 3])
                    with col_img:
                        if r_img:
                            str_app.image(r_img, width=100)
                    with col_txt:
                        str_app.write(f"### {r_item}")
                        str_app.write(f"المتجر: *{r_st}* — السعر: **{r_pr} د.أ** ({r_un})")
            str_app.markdown("---")

        str_app.markdown("### 🏬 أقسام المتجر الرئيسية")
        categories = ["مواد تموينية", "لحوم", "خضار وفواكه", "مطاعم", "حلويات", "مكسرات", "صيدليات"]
        
        cols = str_app.columns(len(categories))
        for idx, cat in enumerate(categories):
            with cols[idx]:
                if str_app.button(cat, use_container_width=True):
                    str_app.session_state.active_category = cat

        active_cat = str_app.session_state.get("active_category", "مواد تموينية")
        str_app.markdown(f"#### 📂 المنتجات المتوفرة في قسم: `{active_cat}`")
        
        c.execute("SELECT name FROM stores WHERE category = ?", (active_cat,))
        stores_in_cat = c.fetchall()
        
        if not stores_in_cat:
            str_app.info("لا توجد متاجر حالياً ضمن هذا القسم.")
        else:
            store_names_list = [s[0] for s in stores_in_cat]
            chosen_store = str_app.selectbox("اختر المتجر المطلوب:", store_names_list)
            
            if chosen_store:
                c.execute("SELECT id, item_name, price, unit_type, image_url FROM products WHERE store_name = ?", (chosen_store,))
                store_prods = c.fetchall()
                
                if not store_prods:
                    str_app.info("لا توجد منتجات مسجلة لهذا المتجر حالياً.")
                else:
                    cart_items = []
                    str_app.markdown("**تصفح المنتجات بالصور الحقيقية وحدد الكميات المطلوبة:**")
                    
                    for p_id, p_name, p_price, p_unit, p_img in store_prods:
                        str_app.markdown("---")
                        col_img, col_info, col_qty = str_app.columns([1, 2, 1])
                        
                        with col_img:
                            if p_img:
                                str_app.image(p_img, width=120)
                            else:
                                str_app.write("📷 (لا توجد صورة)")
                                
                        with col_info:
                            str_app.markdown(f"### {p_name}")
                            str_app.write(f"💵 السعر: **{p_price} د.أ** / {p_unit}")
                            
                        with col_qty:
                            q = str_app.number_input(f"الكمية", min_value=0.0, step=1.0, key=f"q_{p_id}")
                            if q > 0:
                                cart_items.append({"name": p_name, "price": p_price, "qty": q, "total": q * p_price})
                    
                    if cart_items:
                        str_app.markdown("---")
                        str_app.markdown("### 🛒 سلة المشتريات وتفاصيل الفاتورة:")
                        sub_total = sum(i["total"] for i in cart_items)
                        delivery_fee = 1.50
                        service_fee = 0.25
                        grand_total = sub_total + delivery_fee + service_fee
                        
                        for item in cart_items:
                            str_app.write(f"- {item['name']} × {item['qty']} = **{item['total']} د.أ**")
                        
                        str_app.markdown(f"مجموع المشتريات: `{sub_total:.2f} د.أ`")
                        str_app.markdown(f"🚚 أجور التوصيل الثابتة: `{delivery_fee:.2f} د.أ`")
                        str_app.markdown(f"⚙️ رسوم الخدمة الإلكترونية: `{service_fee:.2f} د.أ`")
                        str_app.markdown(f"### 💰 المجموع الكلي النهائي: `{grand_total:.2f} د.أ`")
                        
                        with str_app.form("checkout_order_form"):
                            str_app.markdown("#### طريقة الدفع وتأكيد الطلب:")
                            pay_method = str_app.selectbox("اختر طريقة الدفع:", [
                                "نقداً عند الاستلام",
                                "CliQ - رقم ميرال: 00962797088219 (البنك الإسلامي الأردني)",
                                "CliQ - الحساب: samarza (بنك الاتحاد)"
                            ])
                            confirm_btn = str_app.form_submit_button("تأكيد وإرسال الطلب الآن 🚀")
                            
                            if confirm_btn:
                                items_desc_txt = ", ".join([f"{i['name']} ({i['qty']})" for i in cart_items])
                                c.execute("""
                                    INSERT INTO orders (customer_name, customer_phone, customer_address, store_name, items_desc, sub_total, delivery_fee, service_fee, grand_total, payment_method, order_status, assigned_driver)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'جديد', 'قيد التعيين')
                                """, (str_app.session_state.cust_name, str_app.session_state.cust_phone, str_app.session_state.cust_address, chosen_store, items_desc_txt, sub_total, delivery_fee, service_fee, grand_total, pay_method))
                                conn.commit()
                                
                                str_app.success("✅ تم إرسال طلبك بنجاح!")
                                
                                wa_msg = f"🛒 *طلب جديد عبر منصة واصل بيتك*\n👤 الزبون: {str_app.session_state.cust_name}\n📱 الهاتف: {str_app.session_state.cust_phone}\n📍 العنوان: {str_app.session_state.cust_address}\n🏪 المتجر: {chosen_store}\n📦 الطلبات: {items_desc_txt}\n💰 المجموع الكلي: {grand_total:.2f} د.أ\n💳 الدفع: {pay_method}"
                                encoded_wa_msg = urllib.parse.quote(wa_msg)
                                wa_link = f"https://wa.me/962797088219?text={encoded_wa_msg}"
                                
                                str_app.markdown(f"### 📲 إرسال نسخة من الطلب عبر الواتساب لهاتف ميرال:")
                                str_app.markdown(f"<a href='{wa_link}' target='_blank'><button style='background-color:#25D366; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>اضغط هنا لإرسال تفاصيل الطلب واتساب لميرال (+962797088219)</button></a>", unsafe_allow_html=True)

# ==========================================
# 2. لوحة الإدارة المركزية
# ==========================================
elif portal == "🔔 لوحة الإدارة المركزية":
    str_app.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🔔 لوحة الإدارة والتحكم المركزي</h1>", unsafe_allow_html=True)
    admin_pin = str_app.text_input("أدخل رمز السر للإدارة (محمي):", type="password")
    
    if admin_pin == "1234":
        str_app.success("تم الدخول للوحة الإدارة بنجاح.")
        
        c.execute("SELECT id, customer_name, customer_phone, customer_address, store_name, items_desc, grand_total, payment_method, order_status FROM orders ORDER BY id DESC")
        all_orders = c.fetchall()
        
        admin_sub = str_app.sidebar.radio("خيارات الإدارة:", ["الطلبات الحية", "إدارة السائقين", "إدارة المنتجات والصور"])
        
        if admin_sub == "الطلبات الحية":
            str_app.markdown("### 📋 سجل الطلبات الواردة:")
            if not all_orders:
                str_app.info("لا توجد طلبات مسجلة حتى الآن.")
            else:
                for ord_i in all_orders:
                    o_id, o_cname, o_cphone, o_caddr, o_store, o_items, o_tot, o_pay, o_stat = ord_i
                    with str_app.expander(f"طلب رقم #{o_id} | المتجر: {o_store} | الزبون: {o_cname} | الحالة: [{o_stat}]"):
                        str_app.write(f"📱 **هاتف الزبون:** {o_cphone} | 📍 **العنوان:** {o_caddr}")
                        str_app.write(f"🛒 **الأصناف:** {o_items}")
                        str_app.write(f"💰 **المجموع الكلي:** {o_tot} د.أ ({o_pay})")
                        
                        new_status = str_app.selectbox(f"تحديث حالة الطلب #{o_id}", ["جديد", "قيد التجهيز", "مع السائق", "تم التوصيل"], key=f"stat_sel_{o_id}")
                        if str_app.button(f"حفظ التحديث للطلب #{o_id}", key=f"save_ord_{o_id}"):
                            c.execute("UPDATE orders SET order_status = ? WHERE id = ?", (new_status, o_id))
                            conn.commit()
                            str_app.success("تم تحديث حالة الطلب بنجاح!")
                            str_app.rerun()

        elif admin_sub == "إدارة السائقين":
            str_app.markdown("### 🛵 إدارة أسطول السائقين:")
            c.execute("SELECT id, name, phone, vehicle_type, status FROM drivers")
            drivers = c.fetchall()
            for d in drivers:
                str_app.write(f"- **{d[1]}** | هاتف: {d[2]} | المركبة: {d[3]} | الحالة: **{d[4]}**")
            
            with str_app.form("add_drv"):
                dn = str_app.text_input("اسم السائق الجديد:")
                dp = str_app.text_input("رقم الهاتف:")
                dv = str_app.text_input("نوع المركبة:")
                if str_app.form_submit_button("إضافة سائق"):
                    if dn.strip():
                        c.execute("INSERT INTO drivers (name, phone, vehicle_type, status) VALUES (?, ?, ?, 'متوفر')", (dn.strip(), dp, dv))
                        conn.commit()
                        str_app.success("تم إضافة السائق بنجاح!")
                        str_app.rerun()

        elif admin_sub == "إدارة المنتجات والصور":
            str_app.markdown("### 🏪 إضافة منتج جديد مع صورة العبوة:")
            with str_app.form("add_prod_admin"):
                c.execute("SELECT name FROM stores")
                st_names = [s[0] for s in c.fetchall()]
                p_st = str_app.selectbox("اختر المتجر:", st_names) if st_names else str_app.text_input("أو اسم المتجر:")
                p_name = str_app.text_input("اسم المادة / الصنف:")
                p_price = str_app.number_input("السعر المحلي (د.أ):", min_value=0.1, value=1.0)
                p_unit = str_app.text_input("وحدة القياس:", value="كيلو")
                p_img_url = str_app.text_input("رابط الصورة (Image URL):", placeholder="https://...")
                if str_app.form_submit_button("إضافة الصنف للمنصة"):
                    if p_name.strip():
                        c.execute("INSERT INTO products (store_name, category, item_name, price, unit_type, image_url) VALUES (?, '', ?, ?, ?, ?)", (p_st, p_name.strip(), p_price, p_unit, p_img_url.strip()))
                        conn.commit()
                        str_app.success("تم إضافة الصنف وصورته بنجاح!")
                        str_app.rerun()

    elif admin_pin != "":
        str_app.error("رمز السر خاطئ!")

# ==========================================
# 3. بوابة البائعين والمتاجر
# ==========================================
elif portal == "🏪 بوابة البائعين والمتاجر":
    str_app.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🏪 بوابة البائعين والمتاجر</h1>", unsafe_allow_html=True)
    vendor_pass = str_app.text_input("أدخل كلمة مرور البائعين:", type="password")
    
    if vendor_pass == "5678":
        c.execute("SELECT name FROM stores")
        stores_opt = [s[0] for s in c.fetchall()]
        selected_vendor_store = str_app.selectbox("اختر متجرك:", stores_opt) if stores_opt else None
        
        if selected_vendor_store:
            str_app.info(f"أهلاً بك يا بائع متجر: **{selected_vendor_store}**")
            c.execute("SELECT id, customer_name, customer_phone, customer_address, items_desc, grand_total, payment_method, order_status FROM orders WHERE store_name = ? ORDER BY id DESC", (selected_vendor_store,))
            v_orders = c.fetchall()
            
            if not v_orders:
                str_app.info("لا توجد طلبات واردة لمتجرك حالياً.")
            else:
                for vo in v_orders:
                    v_id, v_cname, v_cphone, v_caddr, v_items, v_tot, v_pay, v_stat = vo
                    with str_app.expander(f"طلب #{v_id} للزبون: {v_cname} — الحالة: [{v_stat}]"):
                        str_app.write(f"📱 هاتف الزبون: {v_cphone} | 📍 العنوان: {v_caddr}")
                        str_app.write(f"🛒 الأصناف: {v_items}")
                        str_app.write(f"💰 المبلغ: {v_tot} د.أ | الدفع: {v_pay}")
                        
                        if str_app.button(f"تأكيد تجهيز الطلبية #{v_id}", key=f"prep_{v_id}"):
                            c.execute("UPDATE orders SET order_status = 'قيد التجهيز' WHERE id = ?", (v_id,))
                            conn.commit()
                            str_app.success("✅ تم تحديث الطلب بنجاح!")
                            str_app.rerun()
    elif vendor_pass != "":
        str_app.error("كلمة مرور البائعين غير صحيحة.")

# ==========================================
# 4. بوابة السائقين
# ==========================================
elif portal == "🛵 بوابة السائقين للتوصيل":
    str_app.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🛵 بوابة السائقين</h1>", unsafe_allow_html=True)
    driver_pass = str_app.text_input("أدخل كلمة مرور السائقين:", type="password")
    
    if driver_pass == "9988":
        driver_name_input = str_app.text_input("اسمك ورقم هاتفك كسائق:")
        if driver_name_input.strip():
            str_app.success(f"أهلاً بك يا كابتن **{driver_name_input}**:")
            c.execute("SELECT id, customer_name, customer_phone, customer_address, store_name, items_desc, grand_total, payment_method, order_status FROM orders WHERE order_status IN ('قيد التجهيز', 'جديد') ORDER BY id DESC")
            delivery_list = c.fetchall()
            
            if not delivery_list:
                str_app.info("لا توجد طلبات جديدة للتوصيل حالياً.")
            else:
                for d_ord in delivery_list:
                    do_id, do_cname, do_cphone, do_caddr, do_store, do_items, do_tot, do_pay, do_stat = d_ord
                    with str_app.expander(f"طلب توصيل #{do_id} من متجر: {do_store} إلى الزبون: {do_cname}"):
                        str_app.write(f"📍 **المتجر:** {do_store} | 📍 **الزبون:** {do_caddr} ({do_cphone})")
                        str_app.write(f"🛒 الأصناف: {do_items} | الإجمالي: {do_tot} د.أ")
                        
                        if str_app.button(f"استلام وتوصيل الطلب #{do_id}", key=f"drv_take_{do_id}"):
                            c.execute("UPDATE orders SET order_status = 'مع السائق' WHERE id = ?", (do_id,))
                            conn.commit()
                            str_app.success("🚀 تم تسجيل استلامك للطلب بنجاح!")
                            str_app.rerun()
    elif driver_pass != "":
        str_app.error("كلمة مرور السائقين غير صحيحة.")

conn.close()