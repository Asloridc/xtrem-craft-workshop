using FluentAssertions;
using MoneyProblem.Domain;
using Xunit;
using static MoneyProblem.Domain.Currency;

namespace MoneyProblem.Tests
{
    public class MoneyTest
    {
        [Fact]
        public void AddInUsdReturnsAValue()
        {
            ((double?)MoneyCalculator.Add(5, USD, 10)).Should()
                .NotBeNull();
        }

        [Fact]
        public void MultiplyInEurosReturnsPositiveNumber()
        {
            MoneyCalculator
                .Times(10, EUR, 2)
                .Should()
                .BeGreaterThanOrEqualTo(0d);
        }

        [Fact]
        public void DivideInKoreanWonsReturnsDouble()
        {
            MoneyCalculator
                .Divide(4002, KRW, 4)
                .Should()
                .Be(1000.5d);
        }
    }
}
