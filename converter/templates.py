#######################################
# ACCOUNT TEMPLATE
#######################################

strTempl_Acc_in = \
"""\
N{strAccountName}
B0.00
D
TCash
^
"""

strTempl_Acc = \
"""\
!Option:AutoSwitch
!Account
{strAccounts}
"""

#######################################
# CATEGORY TEMPLATE
#######################################

strTempl_Cat_in = \
"""\
N{strCategoryName}
D
{strCategoryType}
^
"""

strTempl_Cat = \
"""\
!Clear:AutoSwitch
!Type:Cat
{strCategories}
"""

#######################################
# TRANSACTION TEMPLATE
#######################################

strTempl_trans_in_cat = \
"""\
L{strCategory}{strClass}
"""

strTempl_trans_in_spl = \
"""\
S{strCategory_spl}{strClass}
E{strMemo_spl}
${strValue_spl}
"""

strTempl_trans_in = \
"""\
D{strDate}
P{strPayee}
M{strMemo}
T{strValor}
N{strNumCheck}
{strCategorySplit}\
^
"""

strTempl_trans = \
"""\
!Account
N{strAccount}
B0
D
TCash
^
!Type:Cash
{strTransactions}\
"""