using System;
using analysis;
using System.Threading.Tasks;
using System.Threading;
using System.Collections.Generic;

namespace tutorial
{
    class Program
    {
        static void Run(Object o)
        {
            int i = (int)o;
            Console.WriteLine(i);
            var content = new ResFile(100, 60, 30);
            content.expand("./r" + i + "-d0-result.txt");
            var content2 = new ResFile(100, 60, 30);
            content2.expand("./r" + i + "-d1-result.txt");
            var evts = content.computeEvents();
            Console.WriteLine(evts);
            UInt64 succ = content.checkSuccess(content2);
            var hist = content.genWindowHistogram(content2, 1000);

            using (System.IO.StreamWriter file =
            new System.IO.StreamWriter("./r" + i + "-analysis.txt"))
            {
                file.WriteLine(string.Format("Eb: {0}; Es:{1};En: {2}", evts.Item1, evts.Item2, evts.Item3));
                file.WriteLine(string.Format("Successful Broadcast: {0}", succ));
                foreach (var h in hist)
                {
                    file.WriteLine("{0}:{1}", h.Key, h.Value);
                }


            }

        }
        static void Main(string[] args)
        {
            var pool = new List<Thread>();
            for (int i = 1; i < Int32.Parse(args[0]); i++)
            {
                var t = new Thread(Run);
                t.Start(i);
                pool.Add(t);


            }
            foreach (var p in pool)
            {
                p.Join();
            }


        }
    }
}
