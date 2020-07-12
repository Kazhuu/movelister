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


## The first steps of using Movelister - Master List

When you first open a Movelister-template, it's almost empty of data. So, how to get started using it?

First, you should list all the Actions that you want to make notes of in the Master List. In this context, Action usually means character actions such as attacking or jumping, but on a broader scale it could mean other types of in-game "states" too, such as different states of a menu.

Write down the different Actions in the Action Name-column. Give each Action a compact yet unique name. Optionally, if you want to write a longer name, description or notes about any Action, feel free to use the columns Full Name, Description and Notes 1, Notes 2 and Notes 3 for that purpose.

As for the View and Input List columns, if you just want to get started quickly, feel free to leave them as "Default" for now.

The View-column allows you to split Actions and their mechanics notes into separate groups. For instance, if a game has multiple playable characters, you could give the Actions of each playable character their own View. Movelister can then generate a separate Overview and Details-sheet based on the unique View-names.

The Input List-column indicates which Input List you want to test each Action with. This information is used in the Details-view a bit later on.

Phases-column indicates the complexity of an Action. In fighting game terms, your usual punch animation could have a start-up, active phase and recovery, which would make it 3 Phases. The amount of Phases has some relevance later on when generating a Details-view. If you don't want to fiddle with it too much, feel free to give every Action 3 or 4 Phases, that should be enough for most purposes.

 
Picture 1: Master List with five Actions.

![1](./images/1.PNG?raw=true "Picture 1: Master List with five Actions.")


## The first steps of using Movelister - Inputs

You manage both Inputs and Input Lists from the Inputs-sheet.

Another early step when starting to use Movelister is to list all the relevant Inputs from the game you're making mechanics notes of. While playing the game, pay attention to which Inputs cause changes in character state, then add them to the Input Name-column. It can also be relevant to list some level design elements like water or slippery floor in here too, as they can also cause changes in character state.

Give each Input a compact but unique name. Optionally, you can write down which button corresponds to this Input in the Button-column next to it.

You can group the various Inputs with the Input List-column. If you just want to get started quickly, feel free to leave all the Inputs as "Default". Just keep in mind that it is possible to use different Input Lists for different Actions. For instance, you could make a separate, simplified "Water" Input List for swimming sections so that the mechanics notes for swimming actions will be shorter to read.

Picture 2: The default Input List of Movelister.

![2](./images/2.PNG?raw=true "Picture 2: The default Input List of Movelister.")


## The first steps of using Movelister - Overview pt. 1

Once you have added at least some Actions and Inputs, the next step is generating an Overview. Write the name of some View in the cell C1 in Master List, then press the button to the right to generate an Overview.

So, what is an Overview? You could think of it as a slightly more zoomed-in look at the various Actions that you have listed. Most of the basic info in this sheet is generated based on the info in both Master List and Modifers (which we'll get to later) and shouldn't be modified by hand.

Using the Hit-, Frames- and Notes-columns is optional. The user can indicate which Phase of an Action is "active" and reacts to targets using the Hit-column. Frames-column can be used to list frame data, if needed. And once again, some freeform notes can be written in the Notes-columns.

The most interesting feature of the Overview is the ability to manage Modifiers. Any Modifiers you add in the Modifiers-sheet will also be generated into the Overview upon refreshing it (using the left button). Modifers are an advanced feature of the program you can leave for later if you wish.

The DEF-column is short for "Default". You can use it to generate a vanilla version of an Action in the Details-view without any set up, so it can be helpful for quick testing. Note that every Action you want to generate more detailed notes of needs to have a mark on either DEF or one of the other Modifier-columns, so make sure to leave 'x' or another mark on every Action you want to generate.


Picture 3: A generated Overview with no Modifiers yet.

![3](./images/3.PNG?raw=true "Picture 3: A generated Overview with no Modifiers yet.")


## The first steps of using Movelister - Details

Once you're done, press the right button in the Overview to generate a Details-sheet using the data in the Master List, the current Overview, Inputs-sheet and the previous Details-sheet (if one exists).

Details is the most zoomed-in view for the various Actions, and it's here where you finally write mechanics notes for them. The first three columns Action Name, Modifiers and Input to Compare are automatically filled by Movelister, so don't try to change them by hand.

You write the mechanics notes to columns D and onward. Every three columns, for instance D, E and F, signifies a single Phase of an Action. The Phases are laid out horizontally like this so that you can pay attention to how the rules of an Action change as it progresses. For instance: in many fighting games the recovery or cooldown at the end of an attack has more lenient cancel rules than the previous Phases. Since all of the Action's different Phases can have different rules, they're necessary to list separately like this if you want to be truly systematic about it.

As mentioned, there are three columns reserved for each Phase. The first of these columns holds a Result - it essentially means whether an input cancels, buffers, does nothing, etc. when used during an action - and the column also has a data validation with listed Results in Results-sheet. The purpose of the data validation is that it creates a drop-down menu, allowing you to add data to the mechanics notes faster.

The second column holds the name of an Action. If some input would, for example, cancel an Action, you can use this column to indicate what the next Action will be. This column also has a data validation to make creating notes faster.

The third column holds the name of any Modifiers that are a part of the Action. It can also be used to clarify what an Action will become after a specific Input.

Note: Movelister always generates Phase 0 for all Actions. This should be reserved for simultaneous input tests. For instance, what happens if you simultaneously do a punch and block in some fighting game. Sometimes even this type of results can cause glitches and should be kept track of.


Picture 4: Details-sheet after generation.

![4](./images/3.PNG?raw=true "Picture 4: Details-sheet after generation.")


At this point, you can use Movelister to generate sheets of Actions and Inputs for creating basic mechanics notes. However, to make the most out of Movelister, it helps to understand even more of its functionality, especially Modifiers. Following examples attempt to illustrate situations where Modifiers could be helpful.


### Case example 1:

You are trying to make mechanics notes of a hack 'n' slash game where the character can wield three different weapons. Besides giving the character a different moveset, there's a chance that the currently active weapon also causes other subtle differences in the character mechanics, and you want to get to the bottom of it. In a case like this it's the best to make the three weapons into Modifiers. This way you can easily generate three different versions of any Action for testing these potential differences. Add three Modifiers (WPN1, WPN2, WPN3) in the Modifiers-sheet, refresh Overview, then indicate with 'x' which Actions are compatible with which Modifiers.

The default behavior of Movelister is that all Modifiers will combine with one another automatically. So if you generate the Details-view right now, it will add variations that are probably impossible in-game, such as "Action (WPN1 WPN2)". This is where the Filters-column of the Modifier-sheet comes into play. You could make an Exclusive OR filter which prevents more than one weapon Modifier from appearing at once since it's likely that you cannot wield more than one of the three weapons simultaneously in this hypothetical game. Something like xor(WPN1, WPN2, WPN3) should do the trick.

Also, if you mark an 'x' on the "Required"-column next to the formula, this will further filter all versions of all Actions which don't have at least one of these weapon Modifiers, in case the character never having any weapon at all is also an impossible variation.

Picture 1: Modifier-sheet with three Modifiers and a Filter.

![Example-1](./images/case-1-1.PNG?raw=true "Picture 1: Modifier-sheet with three Modifiers and a Filter.")

Picture 2: Overview-sheet where all compatible Actions are marked with 'x'.

![Example-2](./images/case-1-2.PNG?raw=true "Picture 2: Overview-sheet where all compatible Actions are marked with 'x'.")

Picture 3: The resulting output in the Details-sheet.

![Example-3](./images/case-1-3.PNG?raw=true "Picture 3: The resulting output in the Details-sheet.")


### Case example 2:

You are trying to make mechanics notes of a third-person shooter that has a variety of arm-only Actions which overlap with movement skills such as jumping and crouching. Normally, if you wanted to list all the possible ways these Actions can overlap, you'd have to do it manually: "jump (reload), crouch (reload), jump (switch weapon), crouch (switch weapon)" and so on. But with Modifiers, you could create a Modifier of each arm-only animation, indicate in Overview-sheet which Actions are compatible with which Modifiers with an 'x' and then make a boolean logic filter that prevents impossible combinations of the modifiers from appearing in any Action.


# The different sheets of Movelister

The following sections relate more info about how the individual sheets in Movelister work.

## Master List

This is the sheet where you list all the Actions or other states that you want to make notes of. It has only one button; pressing it will generate a new Overview based on the View-name that you've written in the cell C1.

Note: if you want to rename an Action without a potential loss of data, so far you have to manually find and replace text around the file.


Explanation of various columns:

* View: this column tells the program which View you want to put your notes in. If you just want to get started quickly, feel free to leave everything in this column as Default. An advanced user might want to create more than one View to, for instance, create a separate notes sheet for multiple playable characters.

* Input List: this column tells the program what Input List will be used for an Action when generating a Details-view. If you just want to get started quickly, feel free to leave everything as Default. An advanced user could give, f.e. swimming animations a different, simplified Input List to make water action mechanics notes shorter and easier to maintain.

* Action Name: this column is where you name a given Action. Note that LibreOffice Uno does not differentiate between lower-case and capitalised letters, so use a naming convention that does not rely on caps.

* Color: you can optionally give an Action some color for visual flair. This color will be added to a table in Details-sheet. (TODO: or at least it will be in some future version of this program.)

* Phases: You can note how many different Phases an Action has in the Phases column. For instance, in typical fighting game terms, an attack could have startup, active and recovery - three different Phases. A more complex Action could have even more Phases. From the point of view of mechanics notes, each of these Phases could have unique rules too, and so the wideness of the Details-view will change depending on what is the maximum number of Phases on this column. The number of Phases also adds multiple Rows for an Action in the Overview-sheet to give more precision in setting Modifiers.

* Full Name: optionally, you can add the official / full name for an Action here, if there exists one, if you feel it makes the sheet easier to read.

* Description: optionally, you can add a short description of the Action.

* Notes 1: optionally, you can write some freeform Notes here.


## Overview

This is a generated, named sheet which lists all Actions of a given View. It's a more in-depth view of Actions where you can adjust how they are generated into a Details-sheet, which is where the actual mechanics notes writing happens.

An Overview has two buttons. First button refreshes the Overview. You should always refresh if you've added Actions to the Master List or changed Modifiers in the Modifier-sheet. Second button generates a Details-view with all the Actions listed in the Overview according to the given settings.

Explanation of various columns:

* Action Name: the name of the Action, as it was written in the Master List.

* Hit: this is an optional column that allows you to indicate which part of an Action has "active frames", i.e. when it reacts to enemies or other targets.

* Frames: this is an optional column where you can list the frames of each Phase.

* Phase: this column indicates which Phase the current row of the Action is on.

* DEF: this column is short for "Default". If you want to ignore Movelister's more advanced features with Modifiers and just get to making your notes quickly, you can put an 'x' or another mark here to indicate that you want to generate a vanilla version of this Action in the Details-view. Note that all Actions need to have a mark on either this or following Modifier-columns to be generated in the Details-view at all.

* (Other Modifier columns): these columns appear once you have added any Modifiers in the Modifiers-sheet and then refresh Overview. You can indicate which Actions and Phases are compatible with a Modifier by adding an 'x' or another mark on its column. This impacts how the Action is generated in the Details-sheet as well. By default, all Modifiers that are marked with 'x' combine with each other, resulting in a ton of variations for a single Action, so be careful with adding too many 'x' before you create some filters in the Modifiers-sheet, otherwise you may end up generating a massive Details-sheet by accident (which takes ages).

* Notes 1: optionally, you can make some freeform Notes in the final columns.


## Details

This is a generated, named sheet that also serves as the most in-depth view for Actions in a View. Here the Action is compared against the Input List specified in the Master List and Inputs-sheet and the user can finally get on to creating those mechanics notes.

* Action Name: the name of the Action, as it was written in the Master List.

* Modifiers: this column lists any Modifiers that are a part of the Action. It's essentially a second part of the name of the Action.

* Input to Compare: the Input that you are supposed to test on each row.

* Phase Columns: this is the area for the mechanics notes themselves. Each Phase has three columns reserved for it. The first column should feature a Result (listed in the Results-sheet) indicating if the move is cancelled, buffered, etc. by the Input. The second column features an Action name, indicating which is the new Action (if any) that follows the Input. Third column optionally features a Modifier, in case the new Action has one. To make writing notes easier, each of the columns also has relevant data validation, allowing the user to browse for relevant Results, Actions or Modifiers quickly.


## Inputs

This is a sheet where you list all the Inputs that you want to test game states with. In a typical workflow the user gets started on a decent Input List before generating Details, but it's possible to add more Inputs at any point later on as well.

Note: if you want to rename an Input without a potential loss of data, so far you have to manually find and replace text around the file. Same is true for the various Actions as well.

Explanation of various columns:

* Input List: the name of the current Input List. You can create numerous different Input Lists for different situations by naming them differently.

* Input Name: the name of the input. This is shown in Details-view, so give it a name that makes sense.

* Button: this is an optional column where the user can clarify which button they mean, if it doesn't become apparent from the Input Name already.

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

* Generate Named Ranges: if this option is marked with 'x', then Named Ranges are generated for each Action after generating the Details-sheet. Named Ranges are a handy way to quickly move inside a large sheet, but generating them takes a bit of time, so turning this option off is like a small optimization. TODO: Named Ranges don't work perfectly if there is more than one View and Details-sheet in the file, so in that case turning Named Ranges off can also be a good idea.

* Show entries ascending when generating validation: if this option is marked with 'x', then the data validation for Details-sheet shows the entries in an ascending order instead of the order they are listed in inside the Details-sheet. Ascending order removes duplicates from the list and it can thus make the validation a bit more readable.



## Templates

The two templates are used whenever generating or refreshing Overview or Details. Optimally, the user shouldn't need to do any adjustments to them by hand.


## Other TODO things

* Make manual more in-depth.

* Conditional formatting. Optimally, Movelister should read user input from "Results"-sheet and make a new conditional format every time a new Details is generated to make this sheet easier to read. Other "color" features can also be done around the template using conditional formatting (but only once we learn to harness this mysterious technology with Python).

* Generating input lists. It might be a handy feature for the user to be able to generate an Input List based on certain criteria. For instance, if the user wants to test hit reactions, they could generate an Input List using the 'Hit' column.

* Automatic grouping of Input Lists. You'd have some setting in Inputs which allow automatic creation of groups after Details-generation. This way you could keep less important Inputs folded until the user needs them if they have really large Input Lists.

* Data import / export. If data from a Movelister sheet could be exported to some human-readable text format, it could be shared and versioned more conveniently, allowing multiple people to work on a single project easier. Besides that, having an export / import functionality would also improve the security as this would mean people don't have to share a full LibreOffice Calc template with macros in it, only the data in it.

* Optimizations. Generating very large sheets is slow, but hopefully it can be optimized some way in the future.