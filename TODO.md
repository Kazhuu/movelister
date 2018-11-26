## Details view generation

To generate input list you need to read overview sheet columns to see which modifier columns user has marked with the x letter or something similar. If no x is in the modifier list, then attack will not be printed.

For example if user has attack s1 and x on WPN1 and WPN2, then result to the details list will have action name as attack s1 and modifier column will have both modifiers printed WPN1 + WPN2, WPN1 and WPN2. Basic input list for attack s1 will not be printed because DEF column doesn't have x set.

Above result set can be filtered with boolean logic from modifier list sheet. User can form logical groups in this sheet which will be only valid. Result which will produce false will be left out from the final details list.

To implement above make generator function which will give combination data from the overview sheet based on the placed x values. When that works, then implement functionality which will check if the current combination is valid with the boolean logic. If not then get next result until it's valid. Continue this until generator is exhausted from its data. Generator should give the data in that order that it appears on the details sheet and it can be printed on the fly.
