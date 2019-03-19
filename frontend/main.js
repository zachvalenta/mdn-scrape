var app = new Vue({
	el: '#root',
	data: {
		app: 'CSS fuzzy search',
		results: [],
		query: '',
	},
	methods: {
        search: function(){
            var client = algoliasearch('XIBL2T83F3', 'a9f849eb80ed71aba8938340dd3f63ab');
            var index = client.initIndex('css');
            var results = this.results
            var query = this.query

            if(!query){
                results.length = 0
                return;
            }

            index.search(query, function(err, content) {
                results.length = 0
                for (var i = 0; i <= content.hits.length - 1 ; i++) {
                    hit = content.hits[i]
                    result = {link: hit.link, text: hit.text}
                    results.push(result)
                }
            });
        },
	}
});
