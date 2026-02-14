using System;

namespace Foo {
    class Bar {
        public void M() {
            var x = "hello";
            var y = $"interpolated {name}";
            var z = @"verbatim";
            var w = @class;
        }
    }
}