best_comments_pipeline = [
    {
        '$group': {
            '_id': '$_id',
            'total_score': {
                '$sum': {
                    '$toInt': '$score'
                }
            }
        }
    }, {
        '$sort': {
            'total_score': -1
        }
    }, {
        '$limit': 5
    }
]

short_content_pipeline = [
    {
        '$project': {
            '_id': '$_id',
            'reviewId': '$reviewId',
            'userName': '$userName',
            'userImage': '$userImage',
            'content': '$content',
            'score': '$score',
            'thumbsUpCount': '$thumbsUpCount',
            'reviewCreatedVersion': '$reviewCreatedVersion',
            'at': '$at',
            'replyContent': '$replyContent',
            'length': {
                '$strLenCP': '$content'
            }
        }
    }, {
        '$match': {
            'length': {
                '$lt': 5
            }
        }
    }
]

day_rating_pipeline = [
    {
        '$project': {
            'score': {
                '$toInt': '$score'
            },
            'at': {
                '$dateFromString': {
                    'dateString': '$at'
                }
            }
        }
    }, {
        '$group': {
            '_id': {
                '$dayOfYear': '$at'
            },
            'average': {
                '$avg': '$score'
            }
        }
    }
]