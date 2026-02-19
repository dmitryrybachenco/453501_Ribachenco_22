using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LB5.Domain
{
    public class Car
    {
        public string Number { get; set; } = "";
        public string Brand { get; set; } = "";
        public Engine CarEngine { get; set; } = new Engine();
        public Car() { }
        public Car(string number, string brand, Engine engine)
        {
            Number = number;
            Brand = brand;
            CarEngine = engine;
        }
    }
}
