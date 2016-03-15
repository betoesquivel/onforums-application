#!/usr/bin/env python
'''
The article dictionary ends up in this mongo format


    comment_id : [<e|"#comment-68330010">]
    author : [<content>]
    author_id : [<content>]
    reply_count : [<content>]
    timestamp : [<content>]
    reply_to_author : [<content>]
    reply_to_comment : [<content>]
    content : [<content>]
'''

import pandas as pd
def reverse_comments(article):
    comment_df = pd.DataFrame(article['comments'])
