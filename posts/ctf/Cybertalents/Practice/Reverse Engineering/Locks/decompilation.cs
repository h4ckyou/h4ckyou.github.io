using System;
using System.Security.Cryptography;
using System.Text;

namespace CT_rev_b1
{
	// Token: 0x02000002 RID: 2
	internal class Program
	{
		// Token: 0x06000001 RID: 1 RVA: 0x00002050 File Offset: 0x00000250
		private static string CreateMD5(string input)
		{
			string result;
			using (MD5 md = MD5.Create())
			{
				byte[] bytes = Encoding.ASCII.GetBytes(input);
				byte[] array = md.ComputeHash(bytes);
				StringBuilder stringBuilder = new StringBuilder();
				for (int i = 0; i < array.Length; i++)
				{
					stringBuilder.Append(array[i].ToString("X2"));
				}
				result = stringBuilder.ToString();
			}
			return result;
		}

		// Token: 0x06000002 RID: 2 RVA: 0x000020D0 File Offset: 0x000002D0
		private static void Main(string[] args)
		{
			Console.WriteLine("Pretty simple. eh?, you give me the hash and i`ll be happy :D");
			string text = Console.ReadLine();
			if (text.Length > 11)
			{
				Console.WriteLine("nope!");
				return;
			}
			if (Program.CreateMD5(Environment.UserName + text) != "C246B75690B6F0746AA67ECC9B400ECF")
			{
				Console.WriteLine(":'(");
				return;
			}
			Console.WriteLine(":) thanks");
		}
	}
}
