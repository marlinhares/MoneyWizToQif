

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
!TYPE:Cat
{strCategories}
"""
