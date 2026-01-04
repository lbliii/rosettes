fn first<'a>(s: &'a str) -> &'a str {
    &s[0..1]
}

struct Wrapper<'a> {
    data: &'a str,
}

impl<'a> Wrapper<'a> {
    fn get(&self) -> &'a str {
        self.data
    }
}

fn longest<'a, 'b: 'a>(x: &'a str, y: &'b str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

static STATIC_STR: &'static str = "hello";
