import re


class ContentValidator:

    def validate(self, extracted, document_type):

        tables = extracted["tables"]
        image_count = extracted["imageCount"]

        fields = {}

        # Convert all 2-column table rows into a dictionary
        for table in tables:

            for row in table:

                if len(row) >= 2:

                    key = row[0].replace("*", "").replace(":", "").strip()

                    value = row[1].strip()

                    fields[key] = value

        results = []

        # -----------------------------
        # UAT VALIDATION
        # -----------------------------

        if document_type == "UAT":

            # ---------------- UAT Description ----------------

            description = fields.get("UAT Description", "")

            if len(description.split()) >= 5:

                results.append({
                    "field": "UAT Description",
                    "status": "PASS",
                    "message": "Valid."
                })

            else:

                results.append({
                    "field": "UAT Description",
                    "status": "FAIL",
                    "message": "Minimum 5 words required."
                })

            # ---------------- Test Case Explanation ----------------

            testcase = ""

            for table in tables:

                for row in table:

                    text = " ".join(row)

                    if "Test case Explanation" in text:

                        testcase = text

                        break

            testcase = testcase.replace("Test case Explanation", "")
            testcase = testcase.replace(":", "").strip()

            if len(testcase) > 10:

                results.append({
                    "field": "Test Case Explanation",
                    "status": "PASS",
                    "message": "Valid."
                })

            else:

                results.append({
                    "field": "Test Case Explanation",
                    "status": "FAIL",
                    "message": "Cannot be empty."
                })

            # ---------------- Screenshot ----------------

            if image_count > 0:

                results.append({
                    "field": "Evidence Screenshot",
                    "status": "PASS",
                    "message": f"{image_count} image(s) found."
                })

            else:

                results.append({
                    "field": "Evidence Screenshot",
                    "status": "FAIL",
                    "message": "No screenshot found."
                })

        # ---------------- Overall Status ----------------

        overall = "PASS"

        for item in results:

            if item["status"] == "FAIL":
                overall = "FAIL"

        # ---------------- Governance Score ----------------

        passed = sum(1 for item in results if item["status"] == "PASS")

        score = int((passed / len(results)) * 100) if results else 0

        return {

            "overallStatus": overall,

            "governanceScore": score,

            "results": results

        }