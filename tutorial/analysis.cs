using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Linq;

namespace analysis
{
    class ResFile
    {
        List<char> raw;
        int Tn;
        int Ts;
        int Tb;

        public List<char> Raw { get => raw; set => raw = value; }

        public ResFile(int tn, int trx, int ttx)
        {
            Tn = tn;
            Ts = trx;
            Tb = ttx;
            Raw = new List<char>();


        }

        public void expand(string filename)
        {
            var log = System.IO.File.ReadAllText(filename);
            var evts = log.Split(',');

            Raw = new List<char>();

            foreach (var c in evts)
            {

                if (c == "")
                {
                    continue;
                }
                else if (c.Contains("S"))
                {

                    for (int i = 0; i < Ts; i++)
                    {

                        Raw.Add('S');

                    }



                }
                else if (c.Contains("N"))
                {
                    for (int i = 0; i < Ts; i++)
                    {
                        Raw.Add('N');
                    }
                }
                else if (c.Contains("B"))
                {
                    int n = Int32.Parse(c.Replace('B', ' '));
                    for (int i = 0; i < Tb; i++)
                    {

                        if (i == n)
                        {
                            Raw.Add('B');
                        }
                        else
                        {
                            Raw.Add('X');
                        }


                    }

                }



            }



        }
        public Tuple<int, int, int> computeEvents()
        {
            var Eb = 0;
            var Es = 0;
            var En = 0;

            foreach (char c in Raw)
            {
                switch (c)
                {
                    case 'B':
                        Eb += 1;
                        break;
                    case 'N':
                        En += 1;
                        break;
                    case 'S':
                        Es += 1;
                        break;
                }
            }
            return new Tuple<int, int, int>(Eb, Es / Ts, En / Tn);

        }

        public UInt64 checkSuccess(ResFile vrx)
        {
            UInt64 success = 0;
            for (int i = 0; i < Raw.Count() && i < vrx.Raw.Count(); i++)
            {
                if (Raw[i] == 'B' && vrx.Raw[i] == 'S')
                {
                    success++;
                }


            }
            return success;
        }

        public Dictionary<int, float> genWindowHistogram(ResFile vrx, int wnd)
        {
            var windows = new List<int>();
            for (int i = 0; i < vrx.Raw.Count(); i += wnd)
            {
                var count = 0;
                for (int j = i; j < i + wnd; j++)
                {
                    try
                    {
                        if (Raw[j] == 'B' && vrx.Raw[j] == 'S')
                        {
                            count++;
                        }
                    }
                    catch (Exception e) { }
                }
                windows.Add(count);
            }


            var q = from x in windows
                    group x by x into g
                    let count = g.Count()
                    orderby g.Key
                    select new { Value = g.Key, Count = count };

            Dictionary<int, float> result = new Dictionary<int, float>();
            //TO BE VERIFIED
            foreach (var x in q)
            {
                result.Add(x.Value, (float)x.Count / wnd);
            }

            return result;
        }


    }

}