/*
	Makes sure the heights of panel elements line up
	Assumes that this is applying to dashboards with the class "auto-grid" that contain impact-block
*/
(function(root){

	if(!root.OI) root.OI = {};
	if(!root.OI.ready){
		root.OI.ready = function(fn){
			// Version 1.1
			if(document.readyState != 'loading') fn();
			else document.addEventListener('DOMContentLoaded', fn);
		};
	}
	
	function AlignPanels(el,p){
		var ps = el.querySelectorAll('.impact-block');
		var panels = new Array(ps.length);
		function resize(){
			var rows = {},y,r = 0;

			// Loop over the panels and find the visible children
			for(i = 0; i < ps.length; i++){
				cs = [];
				for(c = 0; c < ps[i].children.length; c++){
					if(ps[i].children[c].offsetParent !== null) cs.push(ps[i].children[c]);
				}
				panels[i] = {'el':ps[i],'children':cs};
			}

			// First calculate which row everything is on
			for(i = 0; i < panels.length; i++){
				y = Math.round(panels[i].el.getBoundingClientRect().y)+"";
				if(!(y in rows)){
					r++;
					rows[y] = {'row':r,'panels':[]};
				}
				rows[y].panels.push(panels[i].el);
			}
			// Loop over each row
			for(r in rows){
				n = 0;
				row = new Array(rows[r].panels.length);
				// Loop over the panels and find the visible children
				for(i = 0; i < rows[r].panels.length; i++){
					cs = [];
					for(c = 0; c < rows[r].panels[i].children.length; c++){
						if(rows[r].panels[i].children[c].offsetParent !== null) cs.push(rows[r].panels[i].children[c]);
					}
					row[i] = {'el':rows[r].panels[i],'children':cs};
					n = Math.max(n,cs.length);
				}

				// Loop over the children of panel
				for(b = 0; b < n; b++){

					maxh = 0;

					// Remove any existing heights that have been set
					for(i = 0; i < row.length; i++){
						temp = row[i].children[b];
						if(temp) temp.style.removeProperty('height');
					}

					// Find the largest height
					for(i = 0; i < row.length; i++){
						temp = row[i].children[b];
						if(temp) maxh = Math.max(maxh,temp.getBoundingClientRect().height);
					}

					// Set all the panels to the maximum height
					for(i = 0; i < row.length; i++){
						temp = row[i].children[b];
						if(temp){
							temp.style.height = maxh+'px';
							row[i].el.setAttribute('data-row',r);
						}
					}
				}

			}

		}
		resize();
		window.addEventListener('resize',resize);
		return this;
	}

	root.OI.AlignPanels = AlignPanels;

})(window || this);

OI.ready(function(){
	var dashboards = document.querySelectorAll('.auto-grid');
	for(var d = 0; d < dashboards.length; d++){
		new OI.AlignPanels(dashboards[d],'.impact-block');
	}
});