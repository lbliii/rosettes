const simple = x => x + 1;

const withParams = (a, b) => a + b;

const withBody = (x) => {
    const y = x * 2;
    return y + 1;
};

const asyncArrow = async (url) => {
    const response = await fetch(url);
    return response.json();
};

const array = [1, 2, 3].map(x => x * 2);
