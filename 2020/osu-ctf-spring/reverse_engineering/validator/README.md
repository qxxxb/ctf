# Super Duper Secure Flag Validator

**Points**: 225

To run:

```sh
java -jar SuperDuperSecureFlagValidator.jar <flag>
```

Problem by: Andrew Haberlandt

## Solution

Using [fernflower](https://github.com/fesh0r/fernflower), a Java decompiler,
I got the following source files:
- [SuperDuperSecureFlagValidator.java](decomp/SuperDuperSecureFlagValidator/SuperDuperSecureFlagValidator.java)
- [Validator1.java](decomp/SuperDuperSecureFlagValidator/Validator1.java)
- [Validator2.java](decomp/SuperDuperSecureFlagValidator/Validator2.java)

`SuperDuperSecureFlagValidator` called `Validator1` and `Validator2` to
verify the user's guess for the flag. The flag consisted of two tokens. The
first was verified by `Validator1` and the second was verified by `Validator2`.

### Validator1

```java
import components.naturalnumber.NaturalNumber;
import components.naturalnumber.NaturalNumber2;
import components.stack.Stack2;

public class Validator1 {
   static boolean verify(String s) {
      if (s.charAt(0) == '0') {
         return false;
      } else {
         NaturalNumber b = new NaturalNumber2(s);
         return secretOp(b, new NaturalNumber2("7109340815511137277436103227634468226488145274050")).equals(new NaturalNumber2("135082787268816958421202995954498890820092905902643"));
      }
   }

   static NaturalNumber secretOp(NaturalNumber a, NaturalNumber b) {
      NaturalNumber two = (NaturalNumber)a.newInstance();
      NaturalNumber three = (NaturalNumber)a.newInstance();
      three.setFromInt(2);
      two.setFromInt(3);
      Stack2 s = new Stack2();

      NaturalNumber z1;
      while(!a.isZero() || !b.isZero()) {
         z1 = a.divide(two);
         NaturalNumber z2 = b.divide(two).divide(three);
         if (z2.isZero()) {
            z1.add(three);
         } else {
            z1.increment();
         }

         z1 = z1.divide(two);
         s.push(z1);
      }

      z1 = (NaturalNumber)a.newInstance();

      while(s.length() > 0) {
         z1.multiply(two);
         z1.add((NaturalNumber)s.pop());
      }

      return z1;
   }
}
```

The token needed to be a string representation of a natural number. This utilized
the [`NaturalNumber`][NaturalNumber] classes from the OSU component library.

The number representation of the token was given to `secretOp()` along with a
second number (similar to a cipher key). The function `secretOp()` returned
another number, which was the result of some mathematical operations on the two
parameters.

In order to get the token, I had to reverse engineer `secretOp()`.  After
attempting to do this for some time, I realized that `two` and `three` were
swapped.

With a little bit of cleanup, the function looked like this:
```java
    static NaturalNumber secretOp(NaturalNumber a, NaturalNumber b) {
        NaturalNumber three = a.newInstance();
        NaturalNumber two = a.newInstance();
        two.setFromInt(2);
        three.setFromInt(3);
        Stack2<NaturalNumber> s = new Stack2<NaturalNumber>();

        NaturalNumber z1;
        while (!a.isZero() || !b.isZero()) {
            z1 = a.divide(three);
            NaturalNumber z2 = b.divide(three).divide(two);
            if (z2.isZero()) {
                z1.add(two);
            } else {
                z1.increment();
            }

            z1 = z1.divide(three);
            s.push(z1);
        }

        z1 = a.newInstance();

        while (s.length() > 0) {
            z1.multiply(three);
            z1.add(s.pop());
        }

        return z1;
    }
```

In the first loop, we divided `a` and `b` by 3 until both reach zero. In the
second loop, we create the result (which I'll denote with `x` from now on) by
repeatedly multiplying it by 3, adding in remainders from dividing `a`.

I rewrote the first loop in pseudo-code in
[secretOp_pseudocode.pdf](secretOp_pseudocode.pdf), showing intermediate
variables and operations.

Since a new element is pushed to the stack on every iteration of the first loop,
we know that the two loops run for the same number of iterations.

The number of iterations is equal to `log_3(max(a, b))`. I wrote this function to
derive it:
```java
    // Using `x` in-place of `a` is not reliable, because it may still be incorrect if
    // `a` is greater than `b`. However, I don't see a solution to this
    static int revSLength(NaturalNumber a, NaturalNumber b) {
        NaturalNumber three = new NaturalNumber2(3);
        NaturalNumber grow = new NaturalNumber2(1);
        int result = 0;

        while (true) {
            boolean greaterThanA = grow.compareTo(a) > 0;
            boolean greaterThanB = grow.compareTo(b) > 0;
            if (greaterThanA && greaterThanB) {
                break;
            }

            grow.multiply(three);
            result++;
        }

        return result;
    }
```

Running `revSLength(a, b)` will give an accurate result. However, we don't know
`a`, because that's what we're trying to solve. Instead, we can use
`revSLength(x, b)`, which should also give an accurate result.

Working backwards in the code, I started reversing the second loop:
```java
        z1 = a.newInstance();

        while (s.length() > 0) {
            z1.multiply(three);
            z1.add(s.pop());
        }
```

Here `z1` is initialized to 0, and then processed in the loop. We know that the
result of `s.pop()` is always one of these values: `{0, 1, 2}` (see
[secretOp_pseudocode.pdf](secretOp_pseudocode.pdf)).

This means that if we repeatedly divide `x` by 3, the remainders will be the
elements of the stack, in reverse order. This makes it possible to generate the
entire stack `s`, just with `x`.
```java
    static Stack2<NaturalNumber> revStack(NaturalNumber x) {
        NaturalNumber three = new NaturalNumber2(3);

        // Clone x
        NaturalNumber x1 = x.newInstance();
        x1.copyFrom(x);

        Stack2<NaturalNumber> result = new Stack2<NaturalNumber>();

        while (!x1.isZero()) {
            // Get remainder
            NaturalNumber r = remainderN(x1, three);

            result.push(r);
            x1.subtract(r);
            x1.divide(three);
        }

        return result;
    }
```

Now that we have the stack `s`, we can try to reverse engineer the first loop.
In turns out that knowing `s` and `b` is enough to allow us to identify a unique
value for `a`.

By following [the pseudo-code](secretOp_pseudocode.pdf), I wrote a function
called `revLoop` to compute the value of `a` on one iteration, and another
overloaded function `revLoop` to compute to calculate `a` across all iterations.

Note: Initially, I didn't think it would give unique values, which is why the
`revLoop()` function returns a `Set` of possible values. I was too lazy to
change it.

```java
    // Calculate `a` for one iteration of the first loop
    static Set1L<NaturalNumber> revLoop(
        NaturalNumber a_rem2,
        NaturalNumber b,
        NaturalNumber a_div // a_next
    ) {
        NaturalNumber three = new NaturalNumber2(3);
        NaturalNumber two = new NaturalNumber2(2);
        NaturalNumber one = new NaturalNumber2(1);

        NaturalNumber b_div = divideN(b, three);
        NaturalNumber b_rem1 = remainderN(b, three);
        NaturalNumber b_rem2 = remainderN(b_rem1, two);

        // Set1L<NaturalNumber> a_rem1_adds = new Set1L<NaturalNumber>();
        Set1L<Integer> a_rem1s = new Set1L<Integer>();

        if (a_rem2.equals(two)) {
            if (b_rem2.isZero()) {
                // a_rem1_adds.add(new NaturalNumber2(2));
                a_rem1s.add(0);
            } else {
                // a_rem1_adds.add(new NaturalNumber2(2));
                a_rem1s.add(1);
            }
        } else if (a_rem2.equals(one)) {
            if (b_rem2.isZero()) {
                // a_rem1_adds.add(new NaturalNumber2(4));
                a_rem1s.add(2);
            } else {
                // a_rem1_adds.add(new NaturalNumber2(1));
                a_rem1s.add(0);
            }
        } else if (a_rem2.isZero()) {
            if (b_rem2.isZero()) {
                // a_rem1_adds.add(new NaturalNumber2(3));
                a_rem1s.add(1);
            } else {
                // a_rem1_adds.add(new NaturalNumber2(3));
                a_rem1s.add(2);
            }
        }

        Set1L<NaturalNumber> result = new Set1L<NaturalNumber>();
        for (int a_rem1 : a_rem1s) {
            // a = (3 * a_div) + a_rem1
            NaturalNumber a = new NaturalNumber2();
            a.copyFrom(a_div);
            a.multiply(three);
            a.add(new NaturalNumber2(a_rem1));

            result.add(a);
        }

        return result;
    }
```

The final step was to combine `revStack` and `revLoop`. During testing, I
noticed that there were cases when the calculated length of the stack `s` and
the number of iterations in the reversal of the first loop were different. This
seemed to occur when there was at least one 0 at the top of stack `s`. To
resolve this, I padded the calculated `s` with zeroes so that its length would
be equal to the result of `revSLength`.

After many hours of work, I was finally able to crack `Validator1`
```sh
$ java_osu SuperValidator
s_length: 106
level: 105
result: {2}
level: 104
result: {7}
level: 103
result: {22}

...

level: 3
result: {11635528346628863846157938456590751422952479256944}
level: 2
result: {34906585039886591538473815369772254268857437770834}
level: 1
result: {104719755119659774615421446109316762806572313312503}
level: 0
result: {314159265358979323846264338327950288419716939937510}
a (gen): 314159265358979323846264338327950288419716939937510

```

### Validator2

```java
import java.util.Base64;

public class Validator2 extends ClassLoader {
   static boolean verify(String s) throws Exception {
      String secret = "yv66vgAAADQAJgoACQATCgAUABUKABQAFggAFwoAFAAYCAAZCgAUABoHABsHABwBAAY8aW5pdD4BAAMoKVYBAARDb2RlAQAPTGluZU51bWJlclRhYmxlAQAGdmVyaWZ5AQAVKExqYXZhL2xhbmcvU3RyaW5nOylaAQANU3RhY2tNYXBUYWJsZQEAClNvdXJjZUZpbGUBAA9WYWxpZGF0b3IyLmphdmEMAAoACwcAHQwAHgAfDAAgACEBAAM3aDIMACIAIwEABDNqazcMACQAJQEAClZhbGlkYXRvcjIBABVqYXZhL2xhbmcvQ2xhc3NMb2FkZXIBABBqYXZhL2xhbmcvU3RyaW5nAQAGbGVuZ3RoAQADKClJAQAJc3Vic3RyaW5nAQAWKElJKUxqYXZhL2xhbmcvU3RyaW5nOwEABmVxdWFscwEAFShMamF2YS9sYW5nL09iamVjdDspWgEABmNoYXJBdAEABChJKUMAIQAIAAkAAAAAAAIAAQAKAAsAAQAMAAAAHQABAAEAAAAFKrcAAbEAAAABAA0AAAAGAAEAAAABAAkADgAPAAEADAAAAHAAAwABAAAANiq2AAIQB58ABQOsKgcQB7YAAxIEtgAFmQAdKgQItgADEga2AAWZAA8qA7YABxBGoAAFBKwDrAAAAAIADQAAAB4ABwAAAAQACQAFAAsABwAaAAgAKAAJADIACgA0AA4AEAAAAAQAAgsoAAEAEQAAAAIAEg==";
      byte[] stuff = Base64.getDecoder().decode(secret);
      Validator2 l = new Validator2();
      Class stuff2 = l.defineClass("Validator2", stuff, 0, stuff.length);
      return (Boolean)stuff2.getMethod("verify", String.class).invoke((Object)null, s);
   }
}
```

Fortunately, it looked much simpler than `Validator1`. The function
`defineClass` dynamically creates a Java class from a `.class` file, which in
this case is expressed as a stream of bytes in `stuff`. I dumped the contents of
`stuff` into a file named `secret.class`, which I then decompiled with [fernflower](https://github.com/fesh0r/fernflower)
```java
public class Validator2 extends ClassLoader {
   public static boolean verify(String var0) {
      if (var0.length() != 7) {
         return false;
      } else {
         return var0.substring(4, 7).equals("7h2") && var0.substring(1, 5).equals("3jk7") && var0.charAt(0) == 'F';
      }
   }
}
```

The correct token was `F3jk7h2`.

### Conclusion

Putting together the tokens for `Validator1` and `Validator2`, the flag was
`osuctf{314159265358979323846264338327950288419716939937510_F3jk7h2}`

[NaturalNumber]: http://web.cse.ohio-state.edu/software/common/doc/components/naturalnumber/package-summary.html
