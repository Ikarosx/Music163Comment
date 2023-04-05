db.getCollection("hot_comment").find({})
db.hot_comment.find({}).sort({likedCount:-1}).pretty()
db.hot_comment.createIndex({likedCount:-1})


db.hot_comment.aggregate([
	{ $group: {
	    _id: { commentId: "$commentId"},
	    dups: {"$addToSet":"$_id"},
	    count: { "$sum": 1}
	}},
	{ $match: {
	    count: {"$gt": 1}
	}}
],{allowDiskUse: true})
.forEach(function(doc){
   doc.dups.shift();
   db.hot_comment.remove({_id: {$in: doc.dups}}); 
});