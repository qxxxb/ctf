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
