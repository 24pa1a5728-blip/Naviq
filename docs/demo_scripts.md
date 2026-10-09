# Naviq Demo Scripts

1. **Passport Fresh**
   - User: "I want to apply for a fresh passport"
   - Expected: Recognizes intent, generates passport fresh RAG plan.

2. **Passport - Missing prerequisite**
   - User: "I want a new passport but I don't have a birth certificate"
   - Expected: Agent identifies `birth_certificate` is missing, lists it in prerequisites.

3. **Driving Licence**
   - User: "I need to get a driving licence"
   - Expected: Returns Sarathi Parivahan RAG plan with Learner's Licence dependency.

4. **Caste Certificate in AP**
   - State dropdown: Andhra Pradesh
   - User: "I want a caste certificate"
   - Expected: Returns MeeSeva details.

5. **Unsupported Service**
   - User: "Book me a flight to Mars"
   - Expected: Returns "unsupported service" message, without inventing a Mars portal.
