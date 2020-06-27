# Movelister User Manual v. 1

## Table of Contents

<!-- vim-markdown-toc GFM -->

* [The Basics](#the-basics)
* [The Different Sheets of Movelister](#the-different-sheets-of-movelister)

<!-- vim-markdown-toc -->


# The Basics

## The idea of Movelister

Movelister is a LibreOffice Calc template with macros for making detailed notes about complex finite-state machines, such as video game characters. It could be convenient for...

- prototyping game logic, for instance if you want to model a game's potential interactivity.
- if you just want to make in-depth mechanics notes about video games.


*Theory: a video game character (and by extension, the video game itself) could be considered to be a complex finite-state machine. It has different states (various actions and moves) which change depending on user-given input.*


## Getting Started

There is no official release of Movelister yet. There is a template that works, but lacks some features and may have bugs - consider it a sort of a 'beta' release. You can find it [here.](https://github.com/Kazhuu/movelister/raw/master/templates/movelister.ods)

Download it and rename it to something more useful, like the name of the game you're making notes of.

Note: only open LibreOffice Calc-sheets with macros from sources you trust, since macros can contain all sorts of dubious code. Hopefully future versions will have a solution regarding this.


## The first steps of using Movelister:

* write down Actions (or other type of states you want to test and make notes of) in the Master List.
* add Inputs to test the Actions with in the Inputs-sheet.
* generate an Overview using the button in the Master List.
* adjust any details in Overview. Put 'x' in the DEF column for each Action (if you're not using any other Modifiers), then press the "Generate Details"-button to generate a Details-view with the selected Actions.
* Once you have generated a Details-view, you can start doing detailed mechanics notes.


However, to make the most out of Movelister, it helps to understand even more of its functionality, especially Modifiers. Following examples attempt to illustrate situations where Modifiers could be helpful.


* Case example 1: you are trying to make mechanics notes of a hack 'n' slash game where the character can wield three different weapons. Besides giving the character a different moveset, there's a chance that the currently active weapon also causes other subtle differences in the character mechanics, and you want to get to the bottom of it. In a case like this it's the best to make the three weapons into Modifiers. This way you can easily generate three different versions of any Action for testing these potential differences. Add three Modifiers (WPN1, WPN2, WPN3) in the Modifiers-sheet, refresh Overview, then indicate with 'x' which Actions are compatible with which Modifiers.

The default behavior of Movelister is that all Modifiers will combine with one another automatically. So if you generate the Details-view right now, it will add variations that are probably impossible in-game, such as "Action (WPN1 WPN2)". This is where the Filters-column of the Modifier-sheet comes into play. You could make an Exclusive OR filter which prevents more than one weapon Modifier from appearing at once since it's likely that you cannot wield more than one of the three weapons simultaneously in this hypothetical game. Something like xor(WPN1, WPN2, WPN3) should do the trick.

Also, if you mark an 'x' on the "Required"-column next to the formula, this will further filter all versions of all Actions which don't have at least one of these weapon Modifiers, in case the character never having any weapon at all is also an impossible variation.

![Example-1](./images/case-1-1.PNG?raw=true "Picture 1: Modifier-sheet with three Modifiers and a Filter.")

![Example-2](./images/case-1-2.PNG?raw=true "Picture 2: Overview-sheet where all compatible Actions are marked with 'x'.")

![Example-3](./images/case-1-3.PNG?raw=true "Picture 3: The resulting output in the Details-sheet.")


* Case example 2: you are trying to make mechanics notes of a third-person shooter that has a variety of arm-only Actions which overlap with movement skills such as jumping and crouching. Normally, if you wanted to list all the possible ways these Actions can overlap, you'd have to do it manually: "jump (reload), crouch (reload), jump (switch weapon), crouch (switch weapon)" and so on. But with Modifiers, you could create a Modifier of each arm-only animation, indicate in Overview-sheet which Actions are compatible with which Modifiers with an 'x' and then make a boolean logic filter that prevents impossible combinations of the modifiers from appearing in any Action.


# The different sheets of Movelister

The following sections relate more info about how the individual sheets in Movelister work.

## Master List

This is the sheet where you list all the Actions, animations or other states that you want to make notes of. It has one button; pressing it will generate a new Overview based on the View-name that you've written in the cell C1.

Explanation of various columns:

* View: this column tells the program what View you want to put your notes in. If you just want to get started quickly, feel free to leave everything in this column as Default. An advanced user might want to create more than one View to, for instance, create a separate notes sheet for multiple playable characters.

* Input List: this column tells the program what Input List will be used for an Action when generating a Details-view. Again, if you just want to get started quickly, feel free to leave everything as Default. An advanced user could give, f.e. swimming animations a different, simplified Input List to make their mechanics notes shorter and easier to maintain.

* Action Name: this column is where you name a given Action. Note that LibreOffice Uno does not differentiate between lower-case and capitalised letters, so create a naming convention that does not rely on caps.

* Color: you can optionally give an Action some color for visual flair. This color will be added to a table in Details-sheet. (TODO: or at least it will be in some future version of this program.)

* Phases: You can note how many different Phases an Action has in the Phases column. For instance, in typical fighting game terms, an attack could have startup, active and recovery - three different Phases. A more complex Action could have even more Phases. From the point of view of mechanics notes, each of these Phases could have unique rules too, and so the wideness of the Details-view will change depending on what is the maximum number of Phases on this column. The number of Phases also adds multiple Rows for an Action in the Overview-sheet to give more precision in setting Modifiers.

* Full Name: you can add the official / full name for an Action here, if there exists one, if you feel it makes the sheet easier to read. It's basically an optional column for the benefit of the user.

* Description: you can add a short description of the Action, if you want. This column is also optional.

* Notes 1: you can write some Notes here. These three columns are also optional.


## Overview

This is a generated, named sheet which lists all Actions of a given View. It's a more in-depth view of Actions where you can adjust how they are generated into a Details-view, where the actual mechanics notes creation happens.

It has two buttons. First button refreshes the Overview. You should always refresh if you've added Actions to the Master List or changed Modifiers in the Modifier-sheet. Second button generates a Details-view with all the Actions listed in the Overview according to the given settings.

Explanation of various columns:

* Action Name: the name of the Action, as it was written in the Master List.

* Hit: this is an optional column that allows you to indicate which part of an Action has "active frames", i.e. when it reacts to enemies or other targets.

* Frames: this is an optional column where you can list the frames of each Phase.

* Phase: this column indicates which Phase the current row of the Action is on.

* DEF: this column is short for "Default". If you want to ignore Movelister's more advanced features with Modifiers and just get to making your notes quickly, you can put an 'x' here to indicate that you want to generate a version of this Action without any other properties in the Details-view. Note that all Actions need to have an 'x' on either this or following Modifier-columns to be generated in the Details-view at all.

* (Other Modifier columns): these columns appear once you have added any Modifiers in the Modifiers-sheet and then refresh Overview. You can indicate which Actions and Phases are compatible with a Modifier by adding an 'x' on its column. This impacts how the Action is generated in the Details-sheet as well. By default, all Modifiers that are marked with 'x' combine with each other, resulting in a ton of variations for a single Action, so be careful with adding too many 'x' before you create some filters in the Modifiers-sheet, otherwise you may end up generating a massive Details-sheet by accident (which takes ages).

* Notes 1: once again, you can make some freeform Notes in the final columns.


## Details

This is a generated, named sheet that also serves as the most in-depth view for Actions in some View. Here the Action is compared against the Input List specified in the Master List and the user can finally get on to creating those mechanics notes.

* Action Name: the name of the Action, as it was written in the Master List.

* Modifiers: this column lists any Modifiers that are a part of the Action. It's essentially a second part of the name of the Action.

* Input to Compare: the Input that you are supposed to test on each row.

* Phase Columns: this is the area for the mechanics notes themselves. Each Phase has three columns reserved for it. The first column should feature a Result (listed in the Results-sheet) indicating if the move is cancelled, buffered, etc. by the Input. The second column features an Action name, indicating which is the new Action (if any) that follows the Input. Third column optionally features a Modifier, in case the new Action has one. To make writing notes easier, each of the columns also has relevant data validation, allowing the user to browse for relevant Results, Actions or Modifiers quickly.



## Inputs

This is a sheet where you list all the Inputs that you want to test game states with. In a typical workflow the user gets started on a decent Input List before generating Details, but it's possible to add more Inputs later on as well.

Note: if you want to rename an Input without a potential loss of data, so far you have to manually find and replace text around the file. Same is true for the various Actions as well.

Explanation of various columns:

* Input List: the name of the current Input List. You can create numerous different Input Lists for different situations by naming them differently.

* Input Name: the name of the input. This is shown in Details-view, so give it a name that makes sense.

* Button: this is an optional column where the user can clarify which button they mean, if it doesn't become apparent from the Input Name already.

* Group: (TODO: in the current version of the program this column does nothing. But it was intended for grouping and folding parts of the Details-sheet to keep it neater after generation. For instance, if the user wanted to generate large swathes of specialized Inputs that might as well be hidden most of the time until they're needed.)

* Color: this is an optional column where the user can give a color for the input. (TODO: in a later version the color will be added to Details-view, but for now it does nothing.)



## Modifiers

This is a sheet where you can create Modifiers. Using Modifiers allows you to generate new Actions according to the rules of boolean logic.

Explanation of various columns:

* Short Name: the name for the Modifier that is used during Details-view generation. In complex projects Actions could get a ton of different Modifiers, so it helps to keep this name as short as possible. Also, don't use a hyphen '-' in Modifier-names because this will confuse the boolean logic.

* Full Name: an optional column where the user can give the Modifier a longer name if they want, just for readability.

* Color: an optional column where the user gives a color to the Modifier. This color is used in Overview, and it can be helpful to visually group different Modifiers based on their type.

* Notes 1: an optional column where the user can write freeform notes about what a Modifier is and what it should do.

* Filters: this column is where you write rules for how the various Modifiers work. To write a filter, either use the available Operators (as listed in the "Operators"-column) or the pre-made Functions (as listed in the "Functions"-column) to indicate how a Modifier can combine with other Modifiers. By default, all Modifiers combine with all other Modifiers, so by using Filters you can cull down the number of combinations to a more manageable amount. Note that the row where you write the formulas on doesn't matter.

* Required: place a mark on this column next to a formula if you want that formula to be true for all generated Actions. See Case Example 1 near the start of this file for a good idea on how to use it.

* Operators: this column lists the available Operators in Movelister, it's just there for user reference.

* Functions: this column lists the available pre-made Functions in Movelister, again, only for user reference.

* Description: this column tells a bit more about what the Functions do, for user reference.



## Results

This sheet lists the various Results of detailed mechanics testing, i.e. whether an Action cancels, buffers, etc. when you do a certain Input during it.

Explanation of various columns:

* List of Results: this column lists existing Results. The user can customize the list however they want. This column is used in Details-sheet when making detailed mechanics notes; the first column in each Phase has data validation that reads this column so that the user can readily access it.

* Color: the user can give a color to a Result and it will show up in the Details-sheet for some visual flair. (TODO: so far the program does not read these colors nor does it generate a new conditional formatting for the Details-sheet whenever the Details is generated again.)

* Explanation for the user: the user can write some freeform notes on these columns.



## About

This sheet features the current version number of Movelister as well as some Options.

Explanation of various options:

(TODO: the color options aren't used in this version of Movelister yet.)

* Show entries ascending when generating validation: if this option is marked with 'x', then the data validation for Details-sheet shows the entries in an ascending order instead of the order they are listed in inside the Details-sheet. Ascending order removes duplicates from the list and it can thus make the validation a bit more readable.



## Templates

The two templates are used whenever generating or refreshing Overview or Details. Optimally, the user shouldn't need to do any adjustments to them by hand.

