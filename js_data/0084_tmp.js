/*
    Structure of data used - 

    CSV parsing - 
    fileData - {
        date:moment(date);
        description:transaction description string;
        amount:number;
    }

    Display cummulative data - 
    [{
        id - index;
        amount - number - index; 
        description - text;
        count - number - amount of transactions with similar description;
        frequency - number - average amount of duration between transactions with similar description in days
        category - string - category to put transactions of one description
    }]

    Display cummulative bar - 
    {
        text - category
        value - amount
    }

    TODO: Add up amount for each category - done

*/