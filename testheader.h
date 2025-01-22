#ifndef TESTHEADER_H
#define TESTHEADER_H


class BigInteger {
private:
    std::vector<int> digits;
    bool isNegative;

public:
    BigInteger(std::string input) : digits({0}){
        if(input[0] == '-') {
            isNegative = true;
            input.erase(input.begin());
        }
        else isNegative = false;

        //reverse push
        for(std::string::iterator it = input.end()-1;it >= input.begin();it--) {
            digits.push_back(*it - '0');
        }

        while(!digits.empty() && digits.back() == 0) {
            digits.pop_back();
        }

        if(digits.empty()) {
            digits.push_back(0);
            isNegative = false;
        }
    }

    std::ostream& operator<<(std::ostream& os) const;

    bool operator==(const BigInteger &input) const;
    bool operator<(const BigInteger &input) const;
    bool operator>(const BigInteger &input) const;
    bool operator<=(const BigInteger &input) const;
    bool operator>=(const BigInteger &input) const;
    bool operator!=(const BigInteger &input) const;

    BigInteger operator+(const BigInteger &input) const;
    BigInteger operator+=(const BigInteger &input) const;
    BigInteger operator++() const;
    BigInteger operator-(const BigInteger &input) const;
    BigInteger operator-=(const BigInteger &input) const;
    BigInteger operator--() const;
    BigInteger operator*(const BigInteger &input) const;
    BigInteger operator*=(const BigInteger &input) const;
    BigInteger operator/(const BigInteger &input) const;
    BigInteger operator/=(const BigInteger &input) const;
    BigInteger operator%(const BigInteger &input) const;
    BigInteger operator%=(const BigInteger &input) const;

    BigInteger divideByTwoForDivision(const BigInteger &input) const;
};

std::ostream& BigInteger::operator<<(std::ostream& os) const{
    std::string result = "";
    if(this->isNegative) {
        result += "-";
    }

    for(auto i = digits.end();i>=digits.begin();i--) {
        result += *i + '0';
    }

    for(auto i : result) {
        std:: cout << i;
    }

    return os;
}

bool BigInteger::operator==(const BigInteger &input) const{
    if(isNegative != input.isNegative || digits.size() != input.digits.size()) {
        return false;
    }

    return this->digits == input.digits;
}

bool BigInteger::operator< (const BigInteger &input) const{
    if (this->isNegative && !input.isNegative) {
        return true;
    }
    else if (!this->isNegative && input.isNegative) {
        return false;
    }
    else if (!this->isNegative && !input.isNegative) {
        if (this->digits.size() < input.digits.size()) {
            return true;
        }
        else if (this->digits.size() > input.digits.size()) {
            return false;
        }

        int inputLength = input.digits.size();
        for (int i=inputLength-1;i>=0;i--) {
            if (this->digits[i] == input.digits[i]) {
                continue;
            }
            else if (this->digits[i] < input.digits[i]) {
                return true;
            }
            else return false;
        }
    }
    else if (this->isNegative && input.isNegative) {
        if (this->digits.size() < input.digits.size()) {
            return false;
        }
        else if (this->digits.size() > input.digits.size()) {
            return true;
        }

        int inputLength = input.digits.size();
        for (int i=inputLength-1;i>=0;i--) {
            if (this->digits[i] == input.digits[i]) {
                continue;
            }
            else if (this->digits[i] < input.digits[i]) {
                return false;
            }
            else return true;
        }
    }

    return false;
}

bool BigInteger::operator>(const BigInteger &input) const{
    return input < *this;
}

bool BigInteger::operator<=(const BigInteger &input) const {
    return (*this < input) || (*this == input);
}

bool BigInteger::operator>=(const BigInteger &input) const{
    return (input < *this) || (*this == input);
}

bool BigInteger::operator!=(const BigInteger &input) const{
    return !(*this == input);
}

BigInteger BigInteger::operator+(const BigInteger &input) const{
    std::string result = "";
    int carry = 0;

    if (this->isNegative && input.isNegative) {
        result += "-";
    }
    else if (!this->isNegative && input.isNegative) {
        return *this - input;
    }
    else if (this->isNegative && input.isNegative) {
        return input - *this;
    }

    int maxsize = std::max(digits.size(), input.digits.size());
    for(int i=0;i<maxsize;++i) {
        int sum = 0;
        int thisvalue = i < digits.size() ? digits[i] : 0;
        int inputvalue = i < input.digits.size() ? input.digits[i] : 0;

        sum = thisvalue + inputvalue + carry;
        result.push_back(sum % 10);
        carry = sum / 10;
    }

    return BigInteger(result);
}

BigInteger BigInteger::operator+=(const BigInteger &input) const {
    return BigInteger(*this + input);
}

BigInteger BigInteger::operator++() const {
    return BigInteger(*this + BigInteger("1"));
}

BigInteger BigInteger::operator-(const BigInteger &input) const {
    if (this->isNegative == input.isNegative) {
        if (*this == input) {
            return BigInteger("0"); // 동일한 숫자는 결과가 0
        }

        const BigInteger *larger;
        const BigInteger *smaller;
        bool resultNegative = false;

        // 자릿수 비교
        if (*this > input) {
            larger = this;
            smaller = &input;
            resultNegative = this->isNegative; // 큰 수의 부호가 결과의 부호
        } else {
            larger = &input;
            smaller = this;
            resultNegative = !this->isNegative; // 작은 수의 부호 반대
        }

        // 뺄셈 알고리즘
        std::vector<int> resultDigits(larger->digits.size(), 0);
        int borrow = 0;

        for (size_t i = 0; i < larger->digits.size(); ++i) {
            int sub = larger->digits[i] - borrow;
            if (i < smaller->digits.size()) {
                sub -= smaller->digits[i];
            }

            if (sub < 0) {
                sub += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }

            resultDigits[i] = sub;
        }

        // 선행 0 제거
        while (resultDigits.size() > 1 && resultDigits.back() == 0) {
            resultDigits.pop_back();
        }

        // 결과 BigInteger 생성
        std::string result = "";
        if(resultNegative) {
            result += "-";
        }

        for(auto i = resultDigits.end();i>=resultDigits.begin();i--) {
            result += *i + '0';
        }

        return result;
    } else {
        // 부호가 다르면 덧셈으로 처리 (A - (-B) == A + B)
        BigInteger temp = input;
        temp.isNegative = !temp.isNegative;
        return *this + temp;
    }
}

BigInteger BigInteger::operator-=(const BigInteger &input) const {
    return BigInteger(*this - input);
}

BigInteger BigInteger::operator--() const {
    return BigInteger(*this - BigInteger("1"));
}

BigInteger BigInteger::operator*(const BigInteger &input) const{
    std::vector<int> resultStorage(this->digits.size() + input.digits.size(), 0);
    std::string result = "";

    for (int i=0;i<this->digits.size();++i) {
        for (int j=0;j<input.digits.size();++j) {
            resultStorage[i+j] += this->digits[i] * input.digits[j];
            if (resultStorage[i+j] > 9) {
                resultStorage[i+j+1] += resultStorage[i+j] / 10;
                resultStorage[i+j] = resultStorage[i+j] % 10;
            }
        }
    }

    int i = resultStorage.size() - 1;
    while (i > 0 && resultStorage[i] == 0) {
        --i;
    }

    if (i == 0 && resultStorage[0] == 0) {
        return BigInteger("0");
    }

    if (this->isNegative != input.isNegative) {
        result += "-";
    }

    for (i; i >= 0; --i) {
        result += (resultStorage[i] + '0');
    }

    return BigInteger(result);
}

BigInteger BigInteger::operator*=(const BigInteger &input) const {
    return BigInteger(*this * input);
}

BigInteger BigInteger::operator/(const BigInteger &input) const{
    if (input == BigInteger("0")) {
        throw std::invalid_argument("Divide by zero is impossible.");
    }

    BigInteger left("0"), right = (*this), mid = divideByTwoForDivision(*this);

    while (left <= right) {
        BigInteger judge = mid * input;
        if (judge == *this) {
            return mid;
        }
        else if (judge > *this) {
            right = mid;
        }
        else {
            left = mid;
        }

        BigInteger newMid = divideByTwoForDivision(left + right);
        if (newMid == mid) {
            break;
        }

        mid = newMid;
    }

    return mid;
}

BigInteger BigInteger::operator/=(const BigInteger &input) const {
    return BigInteger(*this / input);
}

//***
BigInteger BigInteger::operator%(const BigInteger &input) const{
    return BigInteger(*this - (*this / input) * input);
}

BigInteger BigInteger::operator%=(const BigInteger &input) const {
    return BigInteger(*this % input);
}

BigInteger BigInteger::divideByTwoForDivision(const BigInteger &input) const {
    std::string result = "";
    int carry = 0;

    //역순정렬을 방지하기 위해 string -> BigInteger방식 선언, 천만자리를 넘기는 연산이 발생할 경우 유의미
    for (int i = input.digits.size() - 1;i>=0;i--) {
        result += (input.digits[i] + carry) / 2 + '0';
        carry = input.digits[i] % 2;
        carry *= 10;
    }

    return BigInteger(result);
}

#endif //TESTHEADER_H