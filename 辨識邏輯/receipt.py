def receipt_mechine(receipt_num_list,receipt_data):
    if isinstance(receipt_num_list, list) == False:  #辨識 receipt_num_list 的type是否為list
        return("the type of receipt_num should be a list")
    if all(isinstance(sub, str) for sub in receipt_num_list) == False:  #辨識在receipt_num_list中的value是否皆為str
        return("each of the value in receipt_num_list should be a string")
    if 'error' in ['error' for i in receipt_num_list if len(i) != 8]:
        return([(i,'the receipt numbers are not correct') for i in receipt_num_list if len(i) !=8 ])
    else :
        date = receipt_data['日期']
        special_prize = receipt_data['特別獎']
        special_prize_sec = receipt_data['特獎']
        head_prize = receipt_data['頭獎']
        additional_prize = receipt_data['增開六獎']
        total = []
        for receipt_num in receipt_num_list:
            if receipt_num in [x for x in special_prize]:
                c = "特別獎"
                m = '獎金1,000萬元'
                total.append((receipt_num,c,m))
            elif receipt_num in [x for x in special_prize_sec]:
                c = "特獎"
                m = '獎金200萬元'
                total.append((receipt_num,c,m))
            elif receipt_num in [x for x in head_prize]:
                c = "頭獎"
                m = '獎金20萬元'
                total.append((receipt_num,c,m))
            elif receipt_num[1:] in [x[1:] for x in head_prize]:
                c = "二獎"
                m = '獎金4萬元'
                total.append((receipt_num,c,m))
            elif receipt_num[2:] in [x[2:] for x in head_prize]:
                c = "三獎"
                m = '獎金1萬元'
                total.append((receipt_num,c,m))
            elif receipt_num[3:] in [x[3:] for x in head_prize]:
                c = "四獎"
                m = '獎金4千元'
                total.append((receipt_num,c,m))
            elif receipt_num[4:] in [x[4:] for x in head_prize]:
                c = "五獎"
                m = '獎金1千元'
                total.append((receipt_num,c,m))
            elif receipt_num[5:] in [x[5:] for x in head_prize]:
                c = "六獎"
                m = '獎金200元'
                total.append((receipt_num,c,m))
            elif receipt_num[5:] in [x for x in additional_prize]:
                c = "增開六獎"
                m = '獎金200元'
                total.append((receipt_num,c,m))
            else :
                c = '未中獎'
                m = '銘謝惠顧'
                total.append((receipt_num,c,m))
        return total #return(發票號碼,中獎資訊,獲得獎金)
if __name__ == '__main()__':
    receipt_mechine(receipt_num_list,receipt_data)