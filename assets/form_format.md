# Form File Format:

## JSON Format

### First attribute is "firstPage" which has value "start":

### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "firstPage": "start"

### Second attribute is "pages" which has an array of "page" objects:

### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "pages": [ ... ]

##### Each "Page" object has:

1). A page id attribute with the page's id:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; id

2). An array of questions with questions no the page:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; questions

3). A next attribute with the next page's id:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; next

##### Each question in the array of questions has:
 1). A question id attribute:

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "id": "someidhere"

 2). A question  attribute with the question:

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"question": "Some question here?"

 3). A question type attribute with the type of component used:

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"type": (slider/choice/multi-choice)

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3-1). A hasOther attribute indicating if there is an other answer:

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"hasOther": true

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3-2). A range attribute if type is slider:

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"range": [a, b]

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3-3). A answers attribute with an array of possible answers if type is choice or multi-choice:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"answers": ["a", "b", "c"]

### Last next attribute in pages is done:  "next": "done"
