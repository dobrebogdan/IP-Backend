#!/usr/bin/python3

import os.path
from TextClassifier import TextClassifier

data_set_path = os.path.join('data','bbc')
print(data_set_path)
tc = TextClassifier.getTextClassifier(data_set_path)
# tc = TextClassifier.getTextClassifier(data_set_path, forceRecompute=True)

categories, internalCategoryIndexes = tc.predictTexts(
    [
        "bussiness, bussiness stock market lawyer CEO boss employee manager firm board owner founder bussiness",
        "algorithm, technology complexity hardware software bugs software software software software program",
        "gallery concert soccer musical book award audience film",
        "president, law, bill, minister, agriculture, senate, mayor, city",
        "technology computer hardware software websites operate mail email program Microsoft Google PC performance",
        """
            He gave no further clues about its vintage, but the delicate, almost conversational vocals are reminiscent of his more recent live shows.

            Musically, it's spacious and haunting, with a dusting of piano, a sorrowful violin, and slow, brushed percussion - and while interpreting the lyrics would require weeks of scholarship, two lines in particular suggest Dylan may have chosen to release the song now as a commentary on US politics.

            "The day they killed him, someone said to me, 'Son, the age of the Antichrist has just only begun,'" he sings around the nine-minute mark.

            "I said, 'The soul of a nation's been torn away, and it's beginning to go into a slow decay.' And that it's 36 hours past judgement day." 
        """,
        
        """
            On Thursday top US share indexes capped their best three-day gains since the Great Depression.

            It comes as investors expect the US Congress to pass a massive stimulus package by the end of Saturday.

            The Group of 20 (G20) major economies has also pledged to inject over $5 trillion into the global economy.

            Japan's benchmark Nikkei 225 gained 1.6%, the Hang Seng in Hong Kong was up by 1.6% and China's Shanghai Composite rose 1%.

            That followed the Dow Jones Industrial Average and S&P 500 both climbing more than 6% on Wall Street, capping their best three-day streaks since the Great Depression of the 1930s. The tech-heavy Nasdaq ended higher for a second day, up 5.6%.
        """
    ]
)

print(categories)