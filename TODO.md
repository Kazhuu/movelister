## Details view generation

To generate input list you need to read overview sheet columns to see which
modifier columns user has marked with the x letter or something similar. If no x
is in the modifier list, then attack will not be printed.

For example if user has attack s1 and x on WPN1 and WPN2, then result to the
details list will have action name as attack s1 and modifier column will have
both modifiers printed WPN1 + WPN2, WPN1 and WPN2. Basic input list for attack
s1 will not be printed because DEF column doesn't have x set.

Above result set can be filtered with boolean logic from modifier list sheet.
User can form logical groups in this sheet which will be only valid. Result
which will produce false will be left out from the final details list.

## Plan how to implement

From overview sheet create enumerator which will give all different attack and
modifier combinations in order of attack names on the sheet. It could traverse
sheet data and in order from the top. To dedice which combinations leave out
enumarator can be filtered with filter() function. Create API from boolean logic
which implements this filter function and return False on those combinations
which should be left out of the details view. How filter() function is
implemented with boolean logic is not yet fully known, maybe use some library to
do so. After these pieces in place then generate details sheet class instance
from this enumerator.

What type enumerator has and is filtered against is not yet planned. Maybe class
implementing details rows regarding one combination of action and it's
modifiers. Same action with another modifiers is a different instance of this
class. This class could also be held inside of details sheet class to generate
table data in the end.

To get old details sheet information, class created from details sheet should
include afromentioned details classes and have api to check if this details
sheet includes given attack + modifiers information. Maybe store these classes
on dict inside of details sheet class for easier checking them without caring
about the order. This api could be used when enumerator from overview is
iterated over to check if old details include given attack + modifiers combo. If
it includes, pull data from it instead of creating a new one. Before this check
of course if this combination is possible with given boolean combinations.

