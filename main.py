from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
#В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;

pattern = r'^([А-ЯЁа-яё]+)(\s*)(\,?)([А-ЯЁа-яё]+)(\s*)(\,?)([А-ЯЁа-яё]*)(\,?)(\,?)(\,?)'
new_pattern = r'\1\3\10\4\6\9\7\8'
new_contact_list = list()


for name in contacts_list:
    to_string = ','.join(name)
    updated_list = re.sub(pattern, new_pattern, to_string)
    to_list = updated_list.split(',')
    new_contact_list.append(to_list)
# pprint(new_contact_list)

# Привести все телефоны в формат +7(999)999-99-99.
# Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;

pattern2 = r'(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*)(\-*)(\d{3})(\s*)(\-*)(\d{2})(\s*)(\-*)(\d{2})(\s*)(\(*)(доб)*(\.*)(\s*)(\d+)*(\)*)'
new_pattern2 = r'+7(\4)\8-\11-\14\15\17\18\19\20'
new_contact_list2 = list()

for phone in new_contact_list:
    to_string2 = ','.join(phone)
    updated_list2 = re.sub(pattern2, new_pattern2, to_string2)
    to_list2 = updated_list2.split(',')
    new_contact_list2.append(to_list2)

# pprint(new_contact_list2)


# Объединить все дублирующиеся записи о человеке в одну
for contact in new_contact_list2:
    for new_contact in new_contact_list2:
        if contact[0] == new_contact[0] and contact[1] == new_contact[1] and contact is not new_contact:
            if contact[2] == "":
                contact[2] = new_contact[2]
            if contact[3] == "":
                contact[3] = new_contact[3]
            if contact[4] == "":
                contact[4] = new_contact[4]
            if contact[5] == "":
                contact[5] = new_contact[5]
            if contact[6] == "":
                contact[6] = new_contact[6]
                del new_contact[7:]

result_list = list()
for d in new_contact_list2:
    if d not in result_list:
        result_list.append(d)
pprint(result_list)


with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(result_list)
