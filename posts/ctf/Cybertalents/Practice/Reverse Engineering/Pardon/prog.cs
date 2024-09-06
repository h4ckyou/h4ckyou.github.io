public class \u200C\u206C\u206C\u206E\u202B\u200B\u202A\u206A\u202C\u200F\u202A\u200B\u206E\u206B\u200B\u200F\u202E\u200B\u202D\u200B\u202D\u206F\u202E\u200F\u202C\u202A\u200D\u202C\u206D\u200B\u202E\u206B\u202E\u202E\u206A\u202C\u202B\u206D\u200E\u202C\u202E : Exception
{
	// Token: 0x06000008 RID: 8 RVA: 0x0000240C File Offset: 0x0000060C
	public \u200C\u206C\u206C\u206E\u202B\u200B\u202A\u206A\u202C\u200F\u202A\u200B\u206E\u206B\u200B\u200F\u202E\u200B\u202D\u200B\u202D\u206F\u202E\u200F\u202C\u202A\u200D\u202C\u206D\u200B\u202E\u206B\u202E\u202E\u206A\u202C\u202B\u206D\u200E\u202C\u202E()
	{
		Random random = new Random();
		byte[] array = new byte[]
		{
			11,
			1,
			12,
			10,
			54,
			25,
			37,
			36,
			62,
			4,
			62,
			5,
			34,
			58,
			20,
			34,
			56,
			9,
			34,
			4,
			57,
			5,
			44,
			53,
			125,
			63,
			108,
			55,
			34,
			125,
			63,
			55,
			48
		};
		byte b = (byte)random.Next(1, 255);
		byte[] array2 = new byte[array.Length];
		for (int i = 0; i < array.Length; i++)
		{
			array2[i] = (array[i] ^ b);
		}
		throw new NotImplementedException();
	}
}
}
