  data = [
      {
        type: "sunburst",
        labels: unpack(rows, 'labels'),
        parents: (allParents = unpack(rows, 'parents')),
        textfont: {"color": "black"},
        insidetextfont: {"color": "white"},
        // meta: unpack(rows, 'short'),
        hovertext: addBreaks(unpack(rows, 'short')),
        hovertemplate: "%{label}<extra>%{hovertext}</extra>",
        leaf: {"opacity": 0.75},
        marker: {"line": {"width": 3}},
        insidetextorientation: 'radial',
        branchvalues: 'total',
        hoverlabel: {"align": "left"},
      }
  ];