using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Mediator
{
    public interface ISender
    {
        void Send<TRequest>(TRequest request) where TRequest : IRequest;
        TResponse Send<TResponse>(IRequest<TResponse> request);
    }
}
