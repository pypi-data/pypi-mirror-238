from sharetop.core.prepare import BasicTop


token = "9ada862fa17ce574"


if __name__ == '__main__':
    token = "9ada862fa17ce574"
    sharetop_obj = BasicTop(token)
    # print(sharetop_obj)
    d = sharetop_obj.common_exec_func("news_to_normal", {"limit": 10})
    # d = sharetop_obj
    print(d.to_dict("records"))