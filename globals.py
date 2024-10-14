sql_queries = {
    "insert_profile": "INSERT INTO profiles (profile_name,email,password, recovery_email,module_index, module_name, "
                      "proxy_type , proxy_ip, proxy_port, proxy_username, proxy_password, user_agent) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",

    "create_profile": "Create table if not exists profiles (id INTEGER PRIMARY KEY, profile_name TEXT,"
                      "module_index INTEGER, module_name TEXT, email TEXT, password TEXT, recovery_email TEXT,"
                      "proxy_type TEXT, proxy_ip TEXT, proxy_port TEXT, proxy_username TEXT, proxy_password TEXT, "
                      "user_agent TEXT)",

    "update_profile": "UPDATE profiles SET profile_name = ?, email = ?, password = ?, recovery_email = ?, "
                        "module_index = ?, module_name = ?,proxy_type = ?, proxy_ip = ?, proxy_port = ?, proxy_username = ?, "
                        "proxy_password = ?, user_agent = ? WHERE id = ?",

    "delete_profile": "DELETE FROM profiles WHERE id = ?"
}


qt_styles = {
    "btn": {
        "general" : "QPushButton{  border-radius: 1px; background-color: #404040; "
                    "color: white; padding: 5px 10px; border-color: black; border-width: 2px;}"
                    "QPushButton:hover{background-color:#606060;}",
        "normal": "",
        "warning": "",
        "green": "QPushButton:hover{background-color:#003319;}\n"
                 "QPushButton{background-color: #006600; color: white; border-radius: 3px;}"
    }
}

proxy_schemes = ["http", "https", "socks4", "socks5"]