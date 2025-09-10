## 2. OMGG
The application only works in windows, and seems to require relatively high-end hardware due to a lack of optimization. This causes the FPS to be quite low, especially in a virtual machine environment, making the user experience not great.

The current bundle force a game installation every time it is launched, as the generated shortcut appears to not be valid.

We've still been able to run the game provided and test it according to the document that was provided but several problems occurred.

To begin with, we've noticed that a player round could be unintentionally skipped. We've also noticed that even with only 1 sacrifice maximal per turn per player, it is possible to sacrifice more than one if the player is fast enough.

We've also noticed several UI/UX and responsiveness issues, especially when trying to play cards, it could take multiple tries to put the card in the right slot. Additionally, soul and eloquence logos are existent but never defined, meaning that we've had trouble understanding which currency represented what. When opening custom games, we saw that certain parameters could be changed, however there is no clear limit defined and they can get changed without our consent. For example, we tried to play with a maximum amount of soul of 100 but a starting soul number of 200, and the starting soul got lowered to 75 without any warning. Also, while increasing the amount of eloquence gained from 2 to 5 per turn, we've noticed that the text still displayed 2 (while increasing the eloquence by 5).
We also noticed that some cards couldn't be played in the same turn (such as the Mirror of the Damned). This wasn't precised in any description available.

Lastly, when someone the won the game, we found out that the losing party could be stuck in an infinite loop.

The project seem to overall work but it still a few issues that needs to be fixed.